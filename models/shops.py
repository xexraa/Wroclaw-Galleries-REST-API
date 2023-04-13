from db import db

class ShopModel(db.Model):
    __tablename__ = "shops"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)

    store = db.relationship('StoreModel', back_populates='shops')


    
    
    
    
    
    
# class CafeModel(db.Model):
#     __tablename__ = "cafes"
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     store = db.relationship('StoreModel', backref='cafes', lazy=True)

# class RestaurantModel(db.Model):
#     __tablename__ = "restaurants"
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     store = db.relationship('StoreModel', backref='restaurants', lazy=True)

# class ServicePointModel(db.Model):
#     __tablename__ = "service_points"
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     store = db.relationship('StoreModel', backref='service_points', lazy=True)