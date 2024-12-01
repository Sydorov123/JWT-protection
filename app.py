from flask import Flask, jsonify, request
from db import db
from flask_smorest import Api
from resources.item import blp  # зміна з item_blp на blp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)

# Додаємо заголовок API, версію та версію OpenAPI
app.config['API_TITLE'] = 'My Flask API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'  # Додаємо версію OpenAPI

# Налаштування для бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Підключення до бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Налаштування для JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Замість 'your-secret-key' використовуйте ваш секретний ключ
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  # Термін дії токену - 30 днів

# Ініціалізація бази даних та JWT
db.init_app(app)
jwt = JWTManager(app)

# Словник для відкликаних токенів
revoked_tokens = set()

# Обробка помилок для JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

# Перевірка відкликаних токенів
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # Унікальний ідентифікатор токену
    return jti in revoked_tokens

# Логін користувача для отримання токена
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "admin" or password != "adminpassword":
        return jsonify({"msg": "Bad username or password"}), 401
    
    # Генерація токену з терміном дії 30 днів
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=30))
    return jsonify(access_token=access_token)

# Логаут: відкликання поточного токену
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Отримуємо унікальний ідентифікатор токену
    revoked_tokens.add(jti)  # Додаємо його до списку відкликаних
    return jsonify({"message": "Successfully logged out."}), 200

# Ендпоінт для перевірки та відкликання токену
@app.route("/revoke", methods=["POST"])
@jwt_required()
def revoke():
    jti = get_jwt()["jti"]
    if jti in revoked_tokens:
        return jsonify({"message": "This token has already been revoked."}), 400
    
    revoked_tokens.add(jti)
    return jsonify({"message": "Token revoked successfully."}), 200

# Ініціалізація Flask-Smorest для роботи з API
api = Api(app)
api.register_blueprint(blp)  # Використовуємо blp, а не item_blp

if __name__ == '__main__':
    app.run(debug=True)
