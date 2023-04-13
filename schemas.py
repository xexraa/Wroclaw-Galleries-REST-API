from marshmallow import Schema, fields
 

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    free_parking = fields.Bool(required=True)
    number_of_parking_spaces = fields.Int(required=True)
    url = fields.Str(required=True)
    opening_time = fields.Time(required=True)
    closing_time = fields.Time(required=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    postal_code = fields.Str(required=True)


class PlainShopSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    
    
class PlainCafeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ShopSchema(PlainShopSchema):
    store_id = fields.Int(load_only=True, required=True)
 
    
class CafeSchema(PlainCafeSchema):
    store_id = fields.Int(load_only=True, required=True)


class ShopUpdateSchema(Schema):
    name = fields.Str()
    store_id = fields.Int()
    

class CafeUpdateSchema(Schema):
    name = fields.Str()
    store_id = fields.Int()

    
class StoreUpdateSchema(Schema):
    name = fields.Str()
    free_parking = fields.Bool()
    number_of_parking_spaces = fields.Int()
    url = fields.Str()
    opening_time = fields.Time()
    closing_time = fields.Time()
    street = fields.Str()
    city = fields.Str()
    postal_code = fields.Str()
   
        
class StoreSchema(PlainStoreSchema):
    shops = fields.List(fields.Nested(PlainShopSchema(), dump_only=True))
    cafes = fields.List(fields.Nested(PlainCafeSchema(), dump_only=True))


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
   
    
class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)



