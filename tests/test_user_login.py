# test_user_login.py

import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:
    @allure.story("Успешный логин")
    @allure.title("Код 200 при успешном логине")
    def test_login_status_code(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert "success" in response.json()

    @allure.story("Успешный логин")
    @allure.title("Флаг success=True при успешном логине")
    def test_login_success_flag(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert response.json()["success"] is True
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешный логин")
    @allure.title("Наличие accessToken в ответе")
    def test_login_access_token(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert "accessToken" in response.json()
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешный логин")
    @allure.title("Корректный email в ответе")
    def test_login_correct_email(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert response.json()["user"]["email"] == registered_user["email"]
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Неверные данные")
    @allure.title("Неверный пароль: код 401")
    def test_wrong_password_status(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password="invalid_password"
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert not response.json()["success"]

    @allure.story("Неверные данные")
    @allure.title("Неверный пароль: сообщение")
    def test_wrong_password_message(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password="invalid_password"
        )
        assert ERROR_MESSAGES["LOGIN_FAILED"] in response.json()["message"]
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    @allure.story("Неверные данные")
    @allure.title("Несуществующий email: код 401")
    def test_nonexistent_email_status(self, api_client, registered_user):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password=registered_user["password"]
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert not response.json()["success"]

    @allure.story("Неверные данные")
    @allure.title("Несуществующий email: сообщение")
    def test_nonexistent_email_message(self, api_client, registered_user):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password=registered_user["password"]
        )
        assert ERROR_MESSAGES["LOGIN_FAILED"] in response.json()["message"]
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    @allure.story("Неверные данные")
    @allure.title("Неверные данные: код 401")
    def test_invalid_credentials_status(self, api_client):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password="invalid_password"
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert not response.json()["success"]

    @allure.story("Неверные данные")
    @allure.title("Неверные данные: сообщение")
    def test_invalid_credentials_message(self, api_client):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password="invalid_password"
        )
        assert ERROR_MESSAGES["LOGIN_FAILED"] in response.json()["message"]
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]