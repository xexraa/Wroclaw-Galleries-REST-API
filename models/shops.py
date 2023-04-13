from db import db

class ShopModel(db.Model):
    __tablename__ = "shops"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)

    store = db.relationship('StoreModel', back_populates='shops')

