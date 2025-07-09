# test_user_creation.py

import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES
from helpers.generators import remove_field


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    @allure.story("Успешная регистрация")
    @allure.title("Код 200 при успешной регистрации")
    def test_registration_status_code(self, api_client, valid_user_data):
        response = api_client.create_user(**valid_user_data)
        assert response.status_code == HTTP_STATUS["OK"]
        assert "success" in response.json()

    @allure.story("Успешная регистрация")
    @allure.title("Флаг success=True")
    def test_registration_success_flag(self, api_client, valid_user_data):
        response = api_client.create_user(**valid_user_data)
        assert response.json()["success"] is True
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешная регистрация")
    @allure.title("Наличие accessToken")
    def test_registration_access_token(self, api_client, valid_user_data):
        response = api_client.create_user(**valid_user_data)
        assert "accessToken" in response.json()
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешная регистрация")
    @allure.title("Наличие refreshToken")
    def test_registration_refresh_token(self, api_client, valid_user_data):
        response = api_client.create_user(**valid_user_data)
        assert "refreshToken" in response.json()
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешная регистрация")
    @allure.title("Корректный email в ответе")
    def test_registration_correct_email(self, api_client, valid_user_data):
        response = api_client.create_user(**valid_user_data)
        assert response.json()["user"]["email"] == valid_user_data["email"]
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Ошибки регистрации")
    @allure.title("Пустой email: код ошибки")
    def test_empty_email_status(self, api_client, valid_user_data):
        user_data = valid_user_data.copy()
        user_data["email"] = ""
        response = api_client.create_user(**user_data)
        assert response.status_code in [HTTP_STATUS["BAD_REQUEST"], HTTP_STATUS["FORBIDDEN"]]
        assert not response.json()["success"]

    @allure.story("Ошибки регистрации")
    @allure.title("Пустой email: сообщение")
    def test_empty_email_message(self, api_client, valid_user_data):
        user_data = valid_user_data.copy()
        user_data["email"] = ""
        response = api_client.create_user(**user_data)
        assert "email" in response.json()["message"].lower()
        assert response.status_code != HTTP_STATUS["OK"]

    @allure.story("Ошибки регистрации")
    @allure.title("Отсутствие email: код 403")
    def test_missing_email_status(self, api_client, valid_user_data):
        user_data = remove_field(valid_user_data, "email")
        response = api_client.create_user(**user_data)
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]
        assert not response.json()["success"]

    @allure.story("Ошибки регистрации")
    @allure.title("Отсутствие email: сообщение")
    def test_missing_email_message(self, api_client, valid_user_data):
        user_data = remove_field(valid_user_data, "email")
        response = api_client.create_user(**user_data)
        assert ERROR_MESSAGES["REQUIRED_FIELDS"] in response.json()["message"]
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]

    @allure.story("Ошибки регистрации")
    @allure.title("Дубликат пользователя: код 403")
    def test_duplicate_status(self, api_client, registered_user):
        user_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        response = api_client.create_user(**user_data)
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]
        assert not response.json()["success"]

    @allure.story("Ошибки регистрации")
    @allure.title("Дубликат пользователя: сообщение")
    def test_duplicate_message(self, api_client, registered_user):
        user_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        response = api_client.create_user(**user_data)
        assert ERROR_MESSAGES["USER_EXISTS"] in response.json()["message"]
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]