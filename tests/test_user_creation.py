# tests/test_user_creation.py

import allure
import pytest
from helpers.data import HTTP_STATUS


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    # Тесты успешной регистрации
    @allure.story("Успешная регистрация")
    @allure.title("Код ответа 200 при успешной регистрации")
    def test_registration_status_code(self, api_client, generate_unique_user_data):
        response = api_client.create_user(**generate_unique_user_data)
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешная регистрация")
    @allure.title("Флаг success=True при успешной регистрации")
    def test_registration_success_flag(self, api_client, generate_unique_user_data):
        response = api_client.create_user(**generate_unique_user_data)
        assert response.json()["success"] is True

    @allure.story("Успешная регистрация")
    @allure.title("Наличие accessToken в ответе")
    def test_registration_access_token(self, api_client, generate_unique_user_data):
        response = api_client.create_user(**generate_unique_user_data)
        assert "accessToken" in response.json()

    @allure.story("Успешная регистрация")
    @allure.title("Наличие refreshToken в ответе")
    def test_registration_refresh_token(self, api_client, generate_unique_user_data):
        response = api_client.create_user(**generate_unique_user_data)
        assert "refreshToken" in response.json()

    @allure.story("Успешная регистрация")
    @allure.title("Корректный email в ответе")
    def test_registration_correct_email(self, api_client, generate_unique_user_data):
        response = api_client.create_user(**generate_unique_user_data)
        assert response.json()["user"]["email"] == generate_unique_user_data["email"]

    # Тесты ошибок регистрации
    @allure.story("Ошибки регистрации")
    @allure.title("Регистрация с пустым email")
    def test_empty_email_registration(self, api_client, generate_unique_user_data):
        user_data = generate_unique_user_data.copy()
        user_data["email"] = ""
        response = api_client.create_user(**user_data)
        assert response.status_code in [400, 403]
        assert "email" in response.json()["message"].lower()

    @allure.story("Ошибки регистрации")
    @allure.title("Регистрация без email")
    def test_missing_email_registration(self, api_client, generate_unique_user_data):
        user_data = {k: v for k, v in generate_unique_user_data.items() if k != "email"}
        response = api_client.create_user(**user_data)
        assert response.status_code == 403
        assert "required" in response.json()["message"].lower()

    @allure.story("Ошибки регистрации")
    @allure.title("Регистрация существующего пользователя")
    def test_duplicate_registration(self, api_client, registered_user):
        user_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        response = api_client.create_user(**user_data)
        assert response.status_code == HTTP_STATUS["FORBIDDEN"]
        assert "already exists" in response.json()["message"].lower()

    # Тесты валидации данных
    @allure.story("Валидация данных")
    @allure.title("Регистрация с email без @")
    def test_email_without_at_sign(self, api_client, generate_unique_user_data):
        user_data = generate_unique_user_data.copy()
        user_data["email"] = "invalidemail.com"
        response = api_client.create_user(**user_data)
        assert response.status_code in [400, 403, 500]

    @allure.story("Валидация данных")
    @allure.title("API должен отклонять пароль из 1 символа (ожидаемое поведение)")
    @pytest.mark.xfail(reason="Баг в API: принимает пароль из 1 символа", strict=True)
    def test_one_char_password_should_fail(self, api_client, generate_unique_user_data):
        user_data = generate_unique_user_data.copy()
        user_data["password"] = "1"
        response = api_client.create_user(**user_data)
        assert response.status_code != HTTP_STATUS["OK"], (
            "API должен возвращать ошибку при пароле из 1 символа"
        )

    @allure.story("Валидация данных")
    @allure.title("Фактическое поведение API (принимает пароль из 1 символа)")
    def test_one_char_password_current_behavior(self, api_client, generate_unique_user_data):
        user_data = generate_unique_user_data.copy()
        user_data["password"] = "1"
        response = api_client.create_user(**user_data)

        # Проверяем текущее (некорректное) поведение API
        assert response.status_code == HTTP_STATUS["OK"], (
            f"Фактически API вернул {response.status_code}, ожидался 200"
        )
        assert "accessToken" in response.json(), (
            "API неожиданно не вернул токен при коротком пароле"
        )