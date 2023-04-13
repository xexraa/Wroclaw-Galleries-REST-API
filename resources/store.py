from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:storeId>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, storeId):
        store = StoreModel.query.get_or_404(storeId)
        return store
    
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, storeId):
        store = StoreModel.query.get(storeId)
        if store:
            store.name = store_data["name"]
            store.free_parking = store_data["free_parking"]
            store.number_of_parking_spaces = store_data["number_of_parking_spaces"]
            store.url = store_data["url"]
            store.opening_time = store_data["opening_time"]
            store.closing_time = store_data["closing_time"]
            store.street = store_data["street"]
            store.city = store_data["city"]
            store.postal_code = store_data["postal_code"]
        else:
            store = StoreModel(id=storeId, **store_data)           
        db.session.add(store)
        db.session.commit()       
        return store
        
    
    @jwt_required()
    def delete(self, storeId):
        jwt = get_jwt()
        if not jwt.get("isAdmin"):
            abort(401, message="Admin privilege required.")
        store = StoreModel.query.get_or_404(storeId)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}

@blp.route("/store")
class StoreList(MethodView):
    @jwt_required(refresh=True)   
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, storeData):            
        store = StoreModel(**storeData)
        print(store)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred.")
            
        return store