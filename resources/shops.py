from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ShopModel
from schemas import ShopSchema, ShopUpdateSchema

blp = Blueprint("shops", __name__, description="Operations on shops")

@blp.route("/shops/<int:shopsId>")
class Shop(MethodView):
    @blp.response(200, ShopSchema)
    def get(self, shopsId):
        shop = ShopModel.query.get_or_404(shopsId)
        return shop
    
    @blp.arguments(ShopUpdateSchema)
    @blp.response(200, ShopSchema)
    def put(self, shop_data, shopsId):
        shop = ShopModel.query.get(shopsId)
        if shop:
            shop.name = shop_data["name"]
        else:
            shop = ShopModel(id=shopsId, **shop_data)           
        db.session.add(shop)
        db.session.commit()       
        return shop
    
    @jwt_required()
    def delete(self, shopsId):
        jwt = get_jwt()
        if not jwt.get("isAdmin"):
            abort(401, message="Admin privilege required.")
        shop = ShopModel.query.get_or_404(shopsId)
        db.session.delete(shop)
        db.session.commit()
        return {"message": "Attraction deleted."}

@blp.route("/shops")
class ShopList(MethodView):
    @jwt_required(refresh=True)   
    @blp.response(200, ShopSchema(many=True))
    def get(self):
        return ShopModel.query.all()

    @blp.arguments(ShopSchema)
    @blp.response(201, ShopSchema)
    def post(self, shopData):            
        shop = ShopModel(**shopData)
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An attraction already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred.")
            
        return shop