# generators.py

import random
import string
import uuid


def generate_email():
    return f"user{random.randint(1000, 9999)}@example.com"

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_user_data():
    return {
        "email": generate_email(),
        "password": generate_password(),
        "name": f"User{random.randint(100, 999)}"
    }

def generate_unique_user():
    """Новая версия, согласованная с фикстурами"""
    uid = uuid.uuid4().hex[:8]
    return {
        "email": f"user_{uid}@test.com",
        "password": f"Password_{uid}",
        "name": f"User_{uid}"
    }

def remove_field(data: dict, field: str) -> dict:
    """Удаляет указанное поле из словаря"""
    return {k: v for k, v in data.items() if k != field}

def check_error_message(message: str, phrases: list) -> bool:
    """Проверяет наличие фраз в сообщении об ошибке"""
    return any(phrase in message.lower() for phrase in phrases)