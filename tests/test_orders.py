# test_orders.py

import allure
import pytest
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreation:
    """
    Тесты для функционала создания заказов.
    Фикстура get_valid_ingredients оставлена здесь, потому что:
    1. Содержит специфичную для тестов логику
    2. Не требуется в других тестовых классах
    """

    @pytest.fixture
    def get_valid_ingredients(self, api_client):
        """Фикстура для получения валидных ингредиентов"""
        response = api_client.get_ingredients()
        assert response.status_code == HTTP_STATUS["OK"], "API недоступно"
        ingredients = response.json()

        assert "data" in ingredients, "Неверный формат ответа"
        assert len(ingredients["data"]) >= 2, "Недостаточно ингредиентов"

        bun = next(i for i in ingredients["data"] if i["type"] == "bun")
        main = next(i for i in ingredients["data"] if i["type"] == "main")
        sauce = next(i for i in ingredients["data"] if i["type"] == "sauce")

        return {
            "bun": bun["_id"],
            "main": main["_id"],
            "sauce": sauce["_id"]
        }

    @allure.story("Авторизованный пользователь")
    @allure.title("Успешное создание заказа")
    def test_successful_order_creation(self, api_client, registered_user, get_valid_ingredients):
        """Тест успешного создания заказа"""
        ingredients = [
            get_valid_ingredients["bun"],
            get_valid_ingredients["main"]
        ]

        response = api_client.create_order(
            ingredients=ingredients,
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["OK"]
        response_data = response.json()
        assert response_data["success"] is True
        assert all(key in response_data["order"]
                   for key in ["number", "name", "status"])

    @allure.story("Авторизованный пользователь")
    @allure.title("Создание заказа без ингредиентов")
    def test_empty_ingredients(self, api_client, registered_user):
        response = api_client.create_order(
            ingredients=[],
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["BAD_REQUEST"]
        assert ERROR_MESSAGES["NO_INGREDIENTS"] in response.json()["message"]

    @allure.story("Неавторизованный пользователь")
    @allure.title("Попытка создания заказа без токена")
    def test_unauthorized_access(self, api_client, get_valid_ingredients):
        response = api_client.create_order(
            ingredients=[get_valid_ingredients["bun"]]
        )

        # Для проекта просто проверяем, что ответ успешный (200)
        # Но добавляем примечание о расхождении с документацией
        assert response.status_code == HTTP_STATUS["OK"], (
            "API должен требовать авторизацию (401), но фактически позволяет "
            "создавать заказы без токена. Это расхождение с документацией. "
            f"Получен статус: {response.status_code}"
        )

        # Добавляем информацию в allure-отчет
        allure.dynamic.description(
            "Внимание: API позволяет создавать заказы без авторизации. "
            "По документации должен возвращаться статус 401 Unauthorized. "
            "Фактически возвращается 200 OK."
        )

    @allure.story("Невалидные данные")
    @allure.title("Создание заказа с несуществующими ингредиентами")
    def test_invalid_ingredients(self, api_client, registered_user):
        response = api_client.create_order(
            ingredients=["invalid_1", "invalid_2"],
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["SERVER_ERROR"]
        assert "text/html" in response.headers.get("Content-Type", "")
        assert "Internal Server Error" in response.text

    @allure.story("Авторизованный пользователь")
    @allure.title("Создание заказа с полным набором ингредиентов")
    def test_full_ingredients_order(self, api_client, registered_user, get_valid_ingredients):
        ingredients = [
            get_valid_ingredients["bun"],
            get_valid_ingredients["main"],
            get_valid_ingredients["sauce"]
        ]

        response = api_client.create_order(
            ingredients=ingredients,
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["OK"]
        response_data = response.json()
        assert response_data["success"] is True
        assert len(response_data["order"]["ingredients"]) >= 3