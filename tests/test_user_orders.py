import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES

@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestUserOrders:
    @allure.story("Авторизованный пользователь")
    @allure.title("Получение списка заказов")
    def test_get_orders_authorized(self, api_client, registered_user):
        response = api_client.get_user_orders(
            access_token=registered_user["access_token"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert "orders" in response.json()

    @allure.story("Неавторизованный пользователь")
    @allure.title("Попытка получения заказов без авторизации")
    def test_get_orders_unauthorized(self, api_client):
        response = api_client.get_user_orders()
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response.json()["message"] == ERROR_MESSAGES["UNAUTHORIZED"]