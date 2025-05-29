import allure
import pytest
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.story("Авторизованный пользователь")
    @allure.title("Успешное создание заказа")
    def test_successful_order_creation(self, api_client, registered_user, get_valid_ingredients):
        ingredients = [
            get_valid_ingredients["bun"],
            get_valid_ingredients["main"]
        ]

        response = api_client.create_order(
            ingredients=ingredients,
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["success"] is True

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
    @allure.title("API ошибочно разрешает неавторизованные заказы (должен возвращать 401)")
    @pytest.mark.xfail(reason="Баг в API: неавторизованные заказы разрешены", strict=True)
    def test_unauthorized_access_should_fail(self, api_client, get_valid_ingredients):
        response = api_client.create_order(
            ingredients=[get_valid_ingredients["bun"]]
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    @allure.story("Неавторизованный пользователь")
    @allure.title("Фактическое поведение API (разрешает неавторизованные заказы)")
    def test_unauthorized_access_current(self, api_client, get_valid_ingredients):
        response = api_client.create_order(
            ingredients=[get_valid_ingredients["bun"]]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["success"] is True

    @allure.story("Неавторизованный пользователь")
    @allure.title("API ошибочно возвращает success=True (должен быть False)")
    @pytest.mark.xfail(reason="Баг в API: неверный флаг success", strict=True)
    def test_unauthorized_success_flag_should_fail(self, api_client, get_valid_ingredients):
        response = api_client.create_order(
            ingredients=[get_valid_ingredients["bun"]]
        )
        assert not response.json()["success"]

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