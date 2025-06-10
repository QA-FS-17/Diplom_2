# test_user_orders.py

import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestUserOrders:
    @allure.story("Авторизованный пользователь")
    @allure.title("Код 200 при запросе заказов")
    def test_authorized_status_code(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert "success" in response.json()

    @allure.story("Авторизованный пользователь")
    @allure.title("Флаг success=True при запросе заказов")
    def test_authorized_success_flag(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.json()["success"] is True
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Авторизованный пользователь")
    @allure.title("Наличие поля orders в ответе")
    def test_authorized_orders_field(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.story("Авторизованный пользователь")
    @allure.title("Структура заказа при наличии")
    def test_authorized_order_structure(self, api_client, registered_user_with_order):
        response = api_client.get_user_orders(
            access_token=registered_user_with_order["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        orders = response.json().get("orders", [])
        assert isinstance(orders, list)

    @allure.story("Неавторизованный пользователь")
    @allure.title("Код 401 без авторизации")
    def test_unauthorized_status_code(self, api_client):
        response = api_client.get_user_orders()
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert not response.json()["success"]

    @allure.story("Неавторизованный пользователь")
    @allure.title("Сообщение об ошибке без авторизации")
    def test_unauthorized_message(self, api_client):
        response = api_client.get_user_orders()
        assert ERROR_MESSAGES["UNAUTHORIZED"] in response.json()["message"]
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    @allure.story("Граничные случаи")
    @allure.title("Пустой список заказов: код 200")
    def test_empty_list_status_code(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["success"] is True

    @allure.story("Граничные случаи")
    @allure.title("Пустой список заказов: поле orders")
    def test_empty_list_orders_field(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.story("Граничные случаи")
    @allure.title("Пустой список заказов: количество")
    def test_empty_list_length(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert len(response.json()["orders"]) == 0