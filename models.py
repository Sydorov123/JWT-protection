from db import db  # Імпортуємо db з db.py

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        """Метод для повернення JSON-подібної відповіді"""
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        """Знайти елемент за назвою"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, item_id):
        """Знайти елемент за ID"""
        return cls.query.get(item_id)

    def save_to_db(self):
        """Зберегти елемент до бази даних"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Видалити елемент з бази даних"""
        db.session.delete(self)
        db.session.commit()
