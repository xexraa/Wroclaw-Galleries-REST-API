import redis
from rq import Queue
import os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from sqlalchemy import or_

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from tasks import send_user_registration_email

blp = Blueprint("Users", "users", description="Operations on users")
connection = redis.from_url(os.getenv("REDIS_URL"))
queue = Queue("emails", connection=connection)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, userData):
        if UserModel.query.filter(
            or_(                                
                UserModel.username == userData["username"],
                UserModel.email == userData["email"]
                )).first():  
            abort(409, message="A user with that username already exists.")
            
        user = UserModel(username=userData["username"], email=userData["email"], password=pbkdf2_sha256.hash(userData["password"]))
        db.session.add(user)
        db.session.commit()
        
        
        queue.enqueue(send_user_registration_email, user.email, user.username)
        
        return {"message": "User created successfully."}, 201
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, userData):
        user = UserModel.query.filter(UserModel.username == userData["username"]).first()
        if user and pbkdf2_sha256.verify(userData["password"], user.password):
            accessToken = create_access_token(identity=user.id, fresh=True)
            refreshToken = create_refresh_token(identity=user.id)
            return {"accessToken": accessToken, "refreshToken": refreshToken}
        
        abort(401, message="Invalid credentials.")
        
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)     
    def post(self):
        currentUser = get_jwt_identity()
        newToken = create_access_token(identity=currentUser, fresh=False)
        return {"accessToken": newToken}
        
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}

@blp.route("/user/<int:userId>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, userId):
        user = UserModel.query.get_or_404(userId)
        return user
    
    def delete(self, userId):
        user = UserModel.query.get_or_404(userId)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}