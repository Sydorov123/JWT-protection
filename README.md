# Flask JWT Protection API

Це API, розроблене за допомогою Flask, яке забезпечує захист доступу до ресурсів через JWT (JSON Web Token). Користувачі можуть отримати токен після авторизації, який використовується для доступу до захищених маршрутів.

## Основні можливості

- Генерація JWT токенів із терміном дії 30 днів.  
- Захист маршрутів за допомогою JWT.  
- Авторизація через обліковий запис "admin" із паролем "adminpassword".  
- Використання SQLite для зберігання даних.

## Інструкція з встановлення

1. Склонуйте репозиторій:  
    ```bash
    git clone https://your-repository-url.git
    ```

2. Перейдіть до папки проєкту:  
    ```bash
    cd JWT-Protection
    ```

3. Встановіть необхідні залежності:  
    ```bash
    pip install -r requirements.txt
    ```

4. Налаштуйте базу даних:  
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Як запустити

1. Для запуску API використовуйте команду:  
    ```bash
    python run.py
    ```

2. Тепер можна звертатися до API через браузер або Postman.

## Опис функціоналу API

### 1. Авторизація і отримання токена

**Метод**: `POST`  
**Ресурс**: `/login`

**Приклад запиту**:
```json
{
    "username": "admin",
    "password": "adminpassword"
}
```

**Приклад відповіді**:
```json
{
    "access_token": "your-jwt-token"
}
```

### 2. Отримання списку елементів

**Метод**: `GET`  
**Ресурс**: `/item`

**Приклад відповіді**:
```json
[
    {
        "id": 1,
        "name": "Item 1",
        "description": "Description of item 1",
        "price": 19.99
    }
]
```

### 3. Перегляд елемента за його ID

**Метод**: `GET`  
**Ресурс**: `/item/<item_id>`

**Приклад відповіді**:
```json
{
    "id": 1,
    "name": "Item 1",
    "description": "Description of item 1",
    "price": 19.99
}
```

### 4. Створення нового елемента

**Метод**: `POST`  
**Ресурс**: `/item`

**Приклад запиту**:
```json
{
    "name": "Item 2",
    "description": "Description of item 2",
    "price": 29.99
}
```

**Приклад відповіді**:
```json
{
    "id": 2,
    "name": "Item 2",
    "description": "Description of item 2",
    "price": 29.99
}
```

## Типові помилки

- **401 Unauthorized**: Токен не надано або є недійсним.  
- **403 Forbidden**: Токен прострочений.  
- **404 Not Found**: Елемент не знайдено.

#### Розробник: Нікіта Сидоров  
  
