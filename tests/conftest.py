# conftest.py

import pytest
from helpers.api_client import StellarBurgersApi
import uuid


@pytest.fixture
def api_client():
    """Базовая фикстура для работы с API"""
    return StellarBurgersApi()


@pytest.fixture
def generate_unique_user_data():
    """Генерация уникальных данных пользователя"""

    def _generate(prefix=""):
        unique_id = uuid.uuid4().hex[:8]
        return {
            "email": f"{prefix}user_{unique_id}@test.com",
            "password": f"{prefix}Password_{unique_id}",
            "name": f"{prefix}User_{unique_id}"
        }

    return _generate


@pytest.fixture
def registered_user(api_client, generate_unique_user_data):
    """Фикстура создания и удаления тестового пользователя"""
    user_data = generate_unique_user_data()
    response = api_client.create_user(**user_data)

    # Проверяем статус код
    assert response.status_code == 200, f"Не удалось создать пользователя. Status: {response.status_code}"

    # Парсим JSON ответ
    response_data = response.json()
    assert response_data.get('success') is True, "Не удалось создать пользователя"

    # Добавляем токены к данным пользователя
    user_data["access_token"] = response_data.get("accessToken", "")
    user_data["refresh_token"] = response_data.get("refreshToken", "")

    yield user_data

    # Удаление пользователя после теста
    if user_data.get("access_token"):
        delete_response = api_client.delete_user(user_data["access_token"])
        assert delete_response.status_code in [200, 202], "Не удалось удалить пользователя"


@pytest.fixture
def another_registered_user(api_client, generate_unique_user_data):
    """Фикстура для второго тестового пользователя"""
    user_data = generate_unique_user_data(prefix="another_")
    response = api_client.create_user(**user_data)

    assert response.status_code == 200, "Не удалось создать второго пользователя"
    response_data = response.json()

    user_data["access_token"] = response_data["accessToken"]
    yield user_data

    # Удаление пользователя после теста
    delete_response = api_client.delete_user(user_data["access_token"])
    assert delete_response.status_code == 202, "Не удалось удалить второго пользователя"