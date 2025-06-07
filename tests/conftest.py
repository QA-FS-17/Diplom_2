# conftest.py

import pytest
from helpers.api_client import StellarBurgersApi
import uuid
from helpers.data import TestUsers


@pytest.fixture
def api_client():
    return StellarBurgersApi()


@pytest.fixture
def valid_user_data():
    """Генерация валидных данных пользователя"""
    return {
        "email": f"user_{uuid.uuid4().hex[:8]}@test.com",
        "password": f"Password_{uuid.uuid4().hex[:8]}",
        "name": f"User_{uuid.uuid4().hex[:8]}"
    }


@pytest.fixture
def registered_user(api_client, valid_user_data):
    """Основная фикстура зарегистрированного пользователя"""
    response = api_client.create_user(**valid_user_data)
    response_data = response.json()

    user_data = valid_user_data.copy()
    user_data.update({
        "access_token": response_data.get("accessToken", ""),
        "refresh_token": response_data.get("refreshToken", "")
    })

    yield user_data

    if user_data.get("access_token"):
        api_client.delete_user(user_data["access_token"])


@pytest.fixture
def another_registered_user(api_client):
    """Фикстура для второго тестового пользователя"""
    user_data = {
        "email": f"another_{uuid.uuid4().hex[:8]}@test.com",
        "password": f"Password_{uuid.uuid4().hex[:8]}",
        "name": f"User_{uuid.uuid4().hex[:8]}"
    }
    response = api_client.create_user(**user_data)
    response_data = response.json()

    user_data.update({
        "access_token": response_data.get("accessToken", "")
    })

    yield user_data

    if user_data.get("access_token"):
        api_client.delete_user(user_data["access_token"])

@pytest.fixture
def registered_user_with_order(api_client, registered_user, valid_ingredients):
    """Фикстура создания заказа для пользователя"""
    api_client.create_order(
        ingredients=[valid_ingredients["bun"]],
        access_token=registered_user["access_token"]
    )
    return registered_user

@pytest.fixture
def valid_ingredients(api_client):
    """Фикстура для получения валидных ингредиентов"""
    response = api_client.get_ingredients()
    ingredients = response.json()["data"]
    return {
        "bun": next(i["_id"] for i in ingredients if i["type"] == "bun"),
        "main": next(i["_id"] for i in ingredients if i["type"] == "main"),
        "sauce": next(i["_id"] for i in ingredients if i["type"] == "sauce")
    }

@pytest.fixture
def user_creation_data(valid_user_data):
    """Фикстура предоставляет тестовые данные для создания пользователя"""
    return {
        "valid_user": valid_user_data,
        "existing_user": TestUsers.VALID.copy()
    }