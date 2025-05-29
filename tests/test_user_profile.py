# test_user_profile.py

import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES
from helpers.generators import generate_email


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUserProfile:
    # Тесты успешного обновления
    @allure.story("Обновление данных")
    @allure.title("Успешное обновление email")
    def test_update_email(self, api_client, registered_user):
        new_email = generate_email()
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=new_email
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["user"]["email"] == new_email

    @allure.story("Обновление данных")
    @allure.title("Успешное обновление имени")
    def test_update_name(self, api_client, registered_user):
        new_name = "Новое имя"
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            name=new_name
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["user"]["name"] == new_name

    @allure.story("Обновление данных")
    @allure.title("Успешное обновление пароля")
    def test_update_password(self, api_client, registered_user):
        new_password = "NewPassword123!"
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            password=new_password
        )
        assert response.status_code == HTTP_STATUS["OK"]

        # Проверяем, что с новым паролем можно войти
        login_response = api_client.login_user(
            email=registered_user["email"],
            password=new_password
        )
        assert login_response.status_code == HTTP_STATUS["OK"]

    # Тесты ошибок
    @allure.story("Неавторизованный доступ")
    @allure.title("Обновление без токена")
    def test_unauthorized_update(self, api_client):
        response = api_client.update_user_info(
            access_token=None,
            name="Новое имя"
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response.json()["message"] == ERROR_MESSAGES["UNAUTHORIZED"]

    @allure.story("Ошибки валидации")
    @allure.title("Обновление на невалидный email")
    def test_update_invalid_email(self, api_client, registered_user):
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email="invalid-email"
        )
        assert response.status_code in [400, 403]

    @allure.story("Конфликтующие данные")
    @allure.title("Обновление на существующий email")
    def test_update_existing_email(self, api_client, registered_user, another_registered_user):
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=another_registered_user["email"]
        )
        assert response.status_code in [HTTP_STATUS["FORBIDDEN"], HTTP_STATUS["CONFLICT"]]
        assert "already exists" in response.json()["message"].lower()