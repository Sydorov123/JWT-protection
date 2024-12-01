from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)  # Тільки для виведення
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True)  # Додано поле price

class ItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float()  # Додано поле price
