import allure
import pytest
from helpers.data import TestUsers, HTTP_STATUS, ERROR_MESSAGES

@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    # Позитивные сценарии
    @allure.story("Успешная регистрация")
    @allure.title("Статус-код 200 при создании пользователя")
    def test_create_user_status_code(self, api_client):
        response = api_client.create_user(**TestUsers.VALID)
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешная регистрация")
    @allure.title("Флаг success=True при создании пользователя")
    def test_create_user_success_flag(self, api_client):
        response = api_client.create_user(**TestUsers.VALID)
        assert response.json()["success"] is True

    @allure.story("Успешная регистрация")
    @allure.title("Наличие accessToken в ответе")
    def test_create_user_has_token(self, api_client):
        response = api_client.create_user(**TestUsers.VALID)
        assert "accessToken" in response.json()

    # Негативный сценарий: существующий пользователь
    @allure.story("Ошибки регистрации")
    @allure.title("Статус-код 403 при дублировании пользователя")
    def test_duplicate_user_status(self, api_client, registered_user):
        response = api_client.create_user(**TestUsers.VALID)
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]

    @allure.story("Ошибки регистрации")
    @allure.title("Сообщение об ошибке при дублировании пользователя")
    def test_duplicate_user_message(self, api_client, registered_user):
        response = api_client.create_user(**TestUsers.VALID)
        assert response.json()["message"] == ERROR_MESSAGES["USER_EXISTS"]

    # Негативный сценарий: отсутствие полей
    @allure.story("Ошибки регистрации")
    @allure.title("Статус-код 403 при отсутствии поля {field}")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_missing_field_status(self, api_client, field):
        user_data = TestUsers.VALID.copy()
        user_data.pop(field)
        response = api_client.create_user(**user_data)
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]

    @allure.story("Ошибки регистрации")
    @allure.title("Сообщение об ошибке при отсутствии поля {field}")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_missing_field_message(self, api_client, field):
        user_data = TestUsers.VALID.copy()
        user_data.pop(field)
        response = api_client.create_user(**user_data)
        assert ERROR_MESSAGES["REQUIRED_FIELDS"] in response.json()["message"]