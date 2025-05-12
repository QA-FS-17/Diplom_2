# conftest.py

import pytest
from helpers.api_client import StellarBurgersApi
import uuid
import os
import shutil
import time
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для работы с API клиентом"""
    client = StellarBurgersApi()
    yield client


@pytest.fixture
def generate_unique_user_data():
    """Генератор уникальных пользовательских данных с временной меткой"""

    def _generate(prefix=""):
        unique_part = f"{uuid.uuid4().hex[:6]}_{int(time.time() * 1000)}"
        return {
            "email": f"{prefix}user_{unique_part}@test.com",
            "password": f"{prefix}P@ss_{unique_part}",
            "name": f"{prefix}User_{unique_part}"
        }

    return _generate


@pytest.fixture
def registered_user(api_client, generate_unique_user_data):
    """Создание и гарантированное удаление тестового пользователя"""
    user_data = generate_unique_user_data()
    response = None
    try:
        # Создание пользователя
        response = api_client.create_user(**user_data)
        if response.status_code != 200:
            pytest.fail(f"Ошибка создания пользователя: {response.text}")

        response_data = response.json()
        user_data.update({
            "access_token": response_data.get("accessToken", ""),
            "refresh_token": response_data.get("refreshToken", "")
        })

        yield user_data

    finally:
        # Удаление пользователя в любом случае
        if response and response.status_code == 200:
            delete_response = api_client.delete_user(user_data["access_token"])
            if delete_response.status_code not in [200, 202]:
                logger.error(f"Ошибка удаления пользователя: {delete_response.text}")


@pytest.fixture
def another_registered_user(api_client, generate_unique_user_data):
    """Фикстура для второго пользователя с префиксом 'another_'"""
    user_data = generate_unique_user_data(prefix="another_")
    response = api_client.create_user(**user_data)

    if response.status_code != 200:
        pytest.skip("Не удалось создать второго пользователя для теста")

    user_data["access_token"] = response.json().get("accessToken", "")
    yield user_data

    # Удаление после использования
    if user_data.get("access_token"):
        api_client.delete_user(user_data["access_token"])


@pytest.fixture
def valid_ingredients(api_client):
    """Фикстура для получения и проверки валидных ингредиентов"""
    response = api_client.get_ingredients()
    assert response.status_code == 200, "API ингредиентов недоступно"

    ingredients = response.json().get("data", [])
    assert len(ingredients) >= 3, "Недостаточно ингредиентов в базе"

    # Проверка наличия обязательных типов
    required_types = {"bun", "sauce", "main"}
    available_types = {i["type"] for i in ingredients}
    missing_types = required_types - available_types
    assert not missing_types, f"Отсутствуют типы: {', '.join(missing_types)}"

    # Собираем примеры ингредиентов
    return {
        "bun": next(i["_id"] for i in ingredients if i["type"] == "bun"),
        "sauce": next(i["_id"] for i in ingredients if i["type"] == "sauce"),
        "main": next(i["_id"] for i in ingredients if i["type"] == "main")
    }


def pytest_configure(config):
    """Конфигурация окружения для Allure отчетов"""
    allure_dir = os.path.join(os.path.dirname(__file__), "allure_reports")

    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir, ignore_errors=True)

    os.makedirs(allure_dir, exist_ok=True)
    config.option.allure_report_dir = allure_dir


@pytest.fixture(autouse=True)
def cleanup_after_tests(api_client):
    """Автоматическая очистка тестовых данных после каждого теста"""
    yield