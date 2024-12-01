from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

# Створення Blueprint для операцій над елементами
blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()  # Захищаємо цей маршрут за допомогою JWT
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """Отримати елемент за ID"""
        # Пошук елемента за ID в базі даних
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()  # Захищаємо цей маршрут за допомогою JWT
    def delete(self, item_id):
        """Видалити елемент за ID"""
        # Пошук елемента за ID та видалення
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """Оновити елемент за ID"""
        # Оновлення або створення нового елемента, якщо він не існує
        item = ItemModel.query.get_or_404(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            db.session.commit()
            return {"message": "Ура, ти обновив цей елемент!", "item": item}
        else:
            item = ItemModel(**item_data)
            db.session.add(item)
            db.session.commit()
            return {"message": "Ура, ти створив новий елемент!", "item": item}

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()  # Захищаємо цей маршрут за допомогою JWT
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Отримати список усіх елементів"""
        # Повернення списку всіх елементів з бази даних
        return ItemModel.query.all()

    @jwt_required()  # Захищаємо цей маршрут за допомогою JWT
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """Створити новий елемент"""
        # Створення нового елемента та додавання до бази даних
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
            return {"message": "Ура, ти створив новий елемент!", "item": item}
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
