from db import db

class StoreModel(db.Model):
    __tablename__ = "store"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    free_parking = db.Column(db.Boolean, nullable=False)
    number_of_parking_spaces = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(400), nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    street = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False) 
    
    shops = db.relationship('ShopModel', back_populates='store', lazy='dynamic')
    cafes = db.relationship('CafeModel', back_populates='store', lazy='dynamic')


    
    #restaurants
    #service_points
    
    