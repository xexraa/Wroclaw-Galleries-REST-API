from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CafeModel
from schemas import CafeSchema, CafeUpdateSchema

blp = Blueprint("cafes", __name__, description="Operations on cafes")

@blp.route("/cafes/<int:cafesId>")
class Shop(MethodView):
    @blp.response(200, CafeSchema)
    def get(self, cafesId):
        cafe = CafeModel.query.get_or_404(cafesId)
        return cafe
    
    @blp.arguments(CafeUpdateSchema)
    @blp.response(200, CafeSchema)
    def put(self, cafe_data, cafesId):
        cafe = CafeModel.query.get(cafesId)
        if cafe:
            cafe.name = cafe_data["name"]
        else:
            cafe = CafeModel(id=cafesId, **cafe_data)           
        db.session.add(cafe)
        db.session.commit()       
        return cafe
    
    @jwt_required()
    def delete(self, cafesId):
        jwt = get_jwt()
        if not jwt.get("isAdmin"):
            abort(401, message="Admin privilege required.")
        cafe = CafeModel.query.get_or_404(cafesId)
        db.session.delete(cafe)
        db.session.commit()
        return {"message": "Attraction deleted."}

@blp.route("/cafes")
class ShopList(MethodView):
    @jwt_required(refresh=True)   
    @blp.response(200, CafeSchema(many=True))
    def get(self):
        return CafeModel.query.all()

    @blp.arguments(CafeSchema)
    @blp.response(201, CafeSchema)
    def post(self, cafeData):            
        cafe = CafeModel(**cafeData)
        try:
            db.session.add(cafe)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An attraction already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred.")
            
        return cafe