# test_user_orders.py

import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestUserOrders:
    @allure.story("Авторизованный пользователь")
    @allure.title("Получение и проверка списка заказов")
    def test_authorized_order_list(self, api_client, registered_user):
        """Проверка успешного получения заказов с валидацией структуры ответа"""
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )

        # Базовые проверки
        assert response.status_code == HTTP_STATUS["OK"], "Неверный статус-код"
        response_data = response.json()

        # Проверка структуры ответа
        assert "orders" in response_data, "Отсутствует поле orders"
        assert isinstance(response_data["orders"], list), "Orders должен быть списком"

        # Дополнительные проверки, если есть заказы
        if response_data["orders"]:
            order = response_data["orders"][0]
            assert "number" in order, "Заказ должен содержать номер"
            assert "ingredients" in order, "Заказ должен содержать ингредиенты"

    @allure.story("Неавторизованный пользователь")
    @allure.title("Попытка доступа без авторизации")
    def test_unauthorized_access(self, api_client):
        """Проверка обработки неавторизованного доступа"""
        response = api_client.get_user_orders()

        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"], "Неверный статус-код"
        assert response.json()["message"] == ERROR_MESSAGES["UNAUTHORIZED"], "Неверное сообщение об ошибке"

    @allure.story("Граничные случаи")
    @allure.title("Проверка пустого списка заказов")
    def test_empty_order_list(self, api_client, registered_user):
        """Проверка корректной обработки пустого списка заказов"""
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )

        assert response.status_code == HTTP_STATUS["OK"]
        assert "orders" in response.json()
        assert len(response.json()["orders"]) == 0, "Для нового пользователя список заказов должен быть пустым"