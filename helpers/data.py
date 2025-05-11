# data.py

# Конфигурация API
BASE_URL = "https://stellarburgers.nomoreparties.site/api/"

# Ингредиенты для тестов (примеры валидных хешей из документации)
INGREDIENTS = {
    "BUN": "60d3b41abdacab0026a733c6",  # Булка
    "SAUCE": "609646e4dc916e00276b2870",  # Соус
    "MAIN": "60d3b41abdacab0026a733c7",  # Начинка
    "INVALID": "invalid_hash_12345"  # Невалидный хеш
}

# Коды HTTP-статусов
HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "CONFLICT": 409,
    "SERVER_ERROR": 500
}

# Сообщения об ошибках
ERROR_MESSAGES = {
    "USER_EXISTS": "User already exists",
    "REQUIRED_FIELDS": "Email, password and name are required fields",
    "LOGIN_FAILED": "email or password are incorrect",
    "NO_INGREDIENTS": "Ingredient ids must be provided",
    "UNAUTHORIZED": "You should be authorised"
}


# Эндпоинты API
class Endpoints:
    # Авторизация
    REGISTER = "auth/register"
    LOGIN = "auth/login"
    LOGOUT = "auth/logout"
    TOKEN_REFRESH = "auth/token"

    # Профиль пользователя
    USER = "auth/user"

    # Заказы
    ORDERS = "orders"
    ALL_ORDERS = "orders/all"

    # Ингредиенты
    INGREDIENTS = "ingredients"

    # Сброс пароля
    PASSWORD_RESET = "password-reset"
    PASSWORD_RESET_CONFIRM = "password-reset/reset"


# Тестовые данные пользователей
class TestUsers:
    VALID = {
        "email": "test_user@example.com",
        "password": "P@ssw0rd123",
        "name": "Test User"
    }

    INVALID = {
        "wrong_email": {
            "email": "not-an-email",
            "password": "validpass123",
            "name": "User"
        },
        "short_password": {
            "email": "user@example.com",
            "password": "123",
            "name": "User"
        }
    }


# Данные для заказов
class OrderData:
    # Используем реальные ID из API
    VALID = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]  # Пример валидных ID
    INVALID = ["invalid_hash_12345"]
    EMPTY = []