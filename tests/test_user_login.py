# test_user_login.py

import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:
    @allure.story("Успешный логин")
    @allure.title("Проверка успешной авторизации")
    def test_successful_login(self, api_client, registered_user):
        """Проверка всех аспектов успешного входа"""
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )

        # Группа связанных проверок
        assert response.status_code == HTTP_STATUS["OK"]
        response_data = response.json()
        assert response_data["success"] is True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    @allure.story("Неверные данные")
    @allure.title("Неверный пароль")
    def test_wrong_password(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password="invalid_password"
        )

        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR_MESSAGES["LOGIN_FAILED"]

    @allure.story("Неверные данные")
    @allure.title("Несуществующий email")
    def test_nonexistent_email(self, api_client, registered_user):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password=registered_user["password"]
        )

        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response.json()["success"] is False

    @allure.story("Неверные данные")
    @allure.title("Полностью неверные данные")
    def test_invalid_credentials(self, api_client):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password="invalid_password"
        )

        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response.json()["success"] is False