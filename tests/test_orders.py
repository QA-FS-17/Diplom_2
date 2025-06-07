# test_orders.py

import allure
import pytest
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.story("Авторизованный пользователь")
    @allure.title("Успешное создание заказа")
    def test_successful_order_creation(self, api_client, registered_user, valid_ingredients):
        ingredients = [
            valid_ingredients["bun"],
            valid_ingredients["main"]
        ]

        response = api_client.create_order(
            ingredients=ingredients,
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["OK"]
        response_data = response.json()
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert "number" in response_data["order"]

    @allure.story("Авторизованный пользователь")
    @allure.title("Создание заказа без ингредиентов")
    def test_empty_ingredients(self, api_client, registered_user):
        response = api_client.create_order(
            ingredients=[],
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["BAD_REQUEST"]
        response_data = response.json()
        assert response_data["success"] is False
        assert ERROR_MESSAGES["NO_INGREDIENTS"] in response_data["message"]

    @allure.story("Неавторизованный пользователь")
    @allure.title("API ошибочно разрешает неавторизованные заказы (должен возвращать 401)")
    @pytest.mark.xfail(reason="Баг в API: неавторизованные заказы разрешены", strict=True)
    def test_unauthorized_access_should_fail(self, api_client, valid_ingredients):
        response = api_client.create_order(
            ingredients=[valid_ingredients["bun"]]
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        response_data = response.json()
        assert response_data["success"] is False

    @allure.story("Неавторизованный пользователь")
    @allure.title("Фактическое поведение API (разрешает неавторизованные заказы)")
    def test_unauthorized_access_current(self, api_client, valid_ingredients):
        response = api_client.create_order(
            ingredients=[valid_ingredients["bun"]]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        response_data = response.json()
        assert response_data["success"] is True

    @allure.story("Неавторизованный пользователь")
    @allure.title("API ошибочно возвращает success=True (должен быть False)")
    @pytest.mark.xfail(reason="Баг в API: неверный флаг success", strict=True)
    def test_unauthorized_success_flag_should_fail(self, api_client, valid_ingredients):
        response = api_client.create_order(
            ingredients=[valid_ingredients["bun"]]
        )
        response_data = response.json()
        assert not response_data["success"]

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
    def test_full_ingredients_order(self, api_client, registered_user, valid_ingredients):
        ingredients = [
            valid_ingredients["bun"],
            valid_ingredients["main"],
            valid_ingredients["sauce"]
        ]

        response = api_client.create_order(
            ingredients=ingredients,
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["OK"]
        response_data = response.json()
        assert response_data["success"] is True
        assert len(response_data["order"]["ingredients"]) >= 3