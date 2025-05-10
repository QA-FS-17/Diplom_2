import allure
from helpers.data import OrderData, HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreation:
    # С авторизацией
    @allure.story("Авторизованный пользователь")
    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, api_client, registered_user):
        response = api_client.create_order(
            ingredients=OrderData.VALID,
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert "order" in response.json()

    @allure.story("Авторизованный пользователь")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, api_client, registered_user):
        response = api_client.create_order(
            ingredients=OrderData.EMPTY,
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["BAD_REQUEST"]
        assert ERROR_MESSAGES["NO_INGREDIENTS"] in response.json()["message"]

    # Без авторизации
    @allure.story("Неавторизованный пользователь")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, api_client):
        response = api_client.create_order(ingredients=OrderData.VALID)
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    # Невалидные данные
    @allure.story("Невалидные данные")
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, api_client, registered_user):
        response = api_client.create_order(
            ingredients=OrderData.INVALID,
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["SERVER_ERROR"]