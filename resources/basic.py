from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("basic", __name__, description="Operations on stores")


@blp.route("/")
class StoreList(MethodView):  
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()