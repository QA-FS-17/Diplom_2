# test_user_profile.py

import allure
import pytest
from helpers.data import HTTP_STATUS, ERROR_MESSAGES
from helpers.generators import generate_email, check_error_message
import uuid


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUserProfile:
    @allure.story("Обновление данных")
    @allure.title("Успешное обновление email")
    def test_update_email(self, api_client, registered_user):
        new_email = generate_email()
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=new_email
        )
        response_data = response.json()

        assert response.status_code == HTTP_STATUS["OK"]
        assert response_data["success"] is True
        assert response_data["user"]["email"] == new_email

    @allure.story("Обновление данных")
    @allure.title("Успешное обновление имени")
    def test_update_name(self, api_client, registered_user):
        new_name = "Новое имя"
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            name=new_name
        )
        response_data = response.json()

        assert response.status_code == HTTP_STATUS["OK"]
        assert response_data["success"] is True
        assert response_data["user"]["name"] == new_name

    @allure.story("Обновление данных")
    @allure.title("Успешное обновление пароля")
    def test_update_password(self, api_client, registered_user):
        new_password = "NewPassword123!"
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            password=new_password
        )
        response_data = response.json()

        assert response.status_code == HTTP_STATUS["OK"]
        assert response_data["success"] is True

        login_response = api_client.login_user(
            email=registered_user["email"],
            password=new_password
        )
        assert login_response.status_code == HTTP_STATUS["OK"]

    @staticmethod
    def _test_invalid_email(api_client, registered_user, invalid_email):
        """Вспомогательный метод для тестирования невалидных email"""
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=invalid_email
        )
        response_data = response.json()

        assert response.status_code in [HTTP_STATUS["BAD_REQUEST"], HTTP_STATUS["FORBIDDEN"]]
        assert response_data["success"] is False
        assert "email" in response_data["message"].lower()

    @allure.story("Ошибки валидации")
    @allure.title("Попытка задания email без домена")
    @pytest.mark.xfail(reason="Известная проблема API: принимает email без домена верхнего уровня")
    def test_invalid_email_no_domain(self, api_client, registered_user):
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email="missing@domain"
        )
        response_data = response.json()
        assert response.status_code in [HTTP_STATUS["BAD_REQUEST"], HTTP_STATUS["FORBIDDEN"]]
        assert response_data["success"] is False
        assert "email" in response_data["message"].lower()

    @allure.story("Ошибки валидации")
    @allure.title("Попытка задания email без @")
    @pytest.mark.xfail(
        reason="API принимает невалидный email (без символа @). Ожидается ошибка валидации (400), \
        но получаем 200.")
    def test_invalid_email_no_at(self, api_client, registered_user):
        invalid_email = f"invalid-email-{uuid.uuid4()}@test"
        response = api_client.update_user_info(
            registered_user["access_token"],
            invalid_email,
            registered_user["name"]
        )
        assert response.status_code == HTTP_STATUS["BAD_REQUEST"], (
            f"Ожидался статус 400, но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )
        response_data = response.json()
        assert not response_data["success"], "Флаг success должен быть False"
        assert "message" in response_data, "Нет сообщения об ошибке"
        assert "неверный формат email" in response_data[
            "message"].lower(), f"Ожидалось сообщение об ошибке валидации email, \
            но получено: {response_data['message']}"

    @allure.story("Неавторизованный доступ")
    @allure.title("Попытка изменения данных без авторизации")
    def test_unauthorized_update(self, api_client):
        response = api_client.update_user_info(
            access_token=None,
            name="Новое имя"
        )
        response_data = response.json()

        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response_data["success"] is False
        assert response_data["message"] == ERROR_MESSAGES["UNAUTHORIZED"]

    @allure.story("Конфликтующие данные")
    @allure.title("Попытка задания существующего email")
    def test_duplicate_email_update(self, api_client, registered_user, another_registered_user):
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=another_registered_user["email"]
        )
        response_data = response.json()

        assert response.status_code in [HTTP_STATUS["FORBIDDEN"], HTTP_STATUS["CONFLICT"]]
        assert response_data["success"] is False
        assert check_error_message(response_data["message"],
                                   ["already exists", "уже существует"])