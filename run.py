from app import app
from db import db

# Створюємо таблиці в базі даних
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
