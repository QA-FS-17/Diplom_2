# conftest.py

import pytest
from helpers.api_client import StellarBurgersApi
import uuid
from helpers.generators import generate_unique_user
from helpers.data import TestUsers


@pytest.fixture
def api_client():
    return StellarBurgersApi()


@pytest.fixture
def generate_unique_user_data():
    unique_id = uuid.uuid4().hex[:8]
    return {
        "email": f"user_{unique_id}@test.com",
        "password": f"Password_{unique_id}",
        "name": f"User_{unique_id}"
    }


@pytest.fixture
def registered_user(api_client, generate_unique_user_data):
    user_data = generate_unique_user_data
    response = api_client.create_user(**user_data)

    user_data["access_token"] = response.json().get("accessToken", "")
    user_data["refresh_token"] = response.json().get("refreshToken", "")

    yield user_data

    if user_data.get("access_token"):
        api_client.delete_user(user_data["access_token"])


@pytest.fixture
def another_registered_user(api_client, generate_unique_user_data):
    user_data = {
        "email": f"another_{generate_unique_user_data['email']}",
        "password": generate_unique_user_data['password'],
        "name": generate_unique_user_data['name']
    }
    response = api_client.create_user(**user_data)

    user_data["access_token"] = response.json().get("accessToken", "")
    yield user_data

    api_client.delete_user(user_data["access_token"])


@pytest.fixture
def get_valid_ingredients(api_client):
    response = api_client.get_ingredients()
    ingredients = response.json()["data"]

    bun = next(i for i in ingredients if i["type"] == "bun")
    main = next(i for i in ingredients if i["type"] == "main")
    sauce = next(i for i in ingredients if i["type"] == "sauce")

    return {
        "bun": bun["_id"],
        "main": main["_id"],
        "sauce": sauce["_id"]
    }

@pytest.fixture
def user_creation_data():
    """Фикстура предоставляет тестовые данные для создания пользователя"""
    return {
        "valid_user": generate_unique_user(),
        "existing_user": TestUsers.VALID
    }