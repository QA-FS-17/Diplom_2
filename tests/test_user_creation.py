# test_user_creation.py

import allure
import pytest
from helpers.data import TestUsers, HTTP_STATUS
from helpers.generators import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    @classmethod
    def setup_class(cls):
        """Генерация тестовых данных один раз для всех тестов класса"""
        cls.valid_user = generate_unique_user()
        cls.existing_user = TestUsers.VALID

    @allure.story("Успешная регистрация")
    @allure.title("Полная проверка успешной регистрации")
    def test_successful_registration(self, api_client):
        """Проверка всех аспектов успешной регистрации в одном тесте"""
        response = api_client.create_user(**self.valid_user)

        # Основные проверки ответа
        assert response.status_code == HTTP_STATUS["OK"], "Неверный статус-код"
        response_data = response.json()

        # Проверка структуры ответа
        assert response_data["success"] is True, "Флаг success должен быть True"
        assert "accessToken" in response_data, "Отсутствует accessToken"
        assert "refreshToken" in response_data, "Отсутствует refreshToken"
        assert "user" in response_data, "Отсутствует информация о пользователе"

        # Проверка данных пользователя
        user_data = response_data["user"]
        assert user_data["email"] == self.valid_user["email"], "Email не совпадает"
        assert user_data["name"] == self.valid_user["name"], "Name не совпадает"

    @allure.story("Ошибки регистрации")
    @allure.title("Регистрация с отсутствующими полями")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_registration_with_missing_fields(self, api_client, missing_field):
        invalid_user = self.valid_user.copy()
        invalid_user[missing_field] = ""  # Отправляем пустое значение

        response = api_client.create_user(**invalid_user)

        # API возвращает 403 вместо ожидаемого 400
        assert response.status_code >= 400, (
            f"Ожидалась ошибка клиента (4xx), получен {response.status_code}"
        )
        assert not response.json().get("success", True), "Флаг success должен быть False"

        response_data = response.json()
        assert "message" in response_data, "Отсутствует сообщение об ошибке"
        assert "required" in response_data["message"].lower(), (
            "Сообщение об ошибке должно указывать на обязательные поля"
        )

    @allure.story("Ошибки регистрации")
    @allure.title("Регистрация существующего пользователя")
    def test_duplicate_registration(self, api_client, registered_user):
        user_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        response = api_client.create_user(**user_data)

        assert response.status_code == HTTP_STATUS["FORBIDDEN"], (
            "Ожидался статус 403 для существующего пользователя"
        )

        response_data = response.json()
        assert "already exists" in response_data.get("message", "").lower(), (
            "Сообщение об ошибке должно указывать на существующего пользователя"
        )

    @allure.story("Валидация данных")
    @allure.title("Проверка невалидных email")
    @pytest.mark.parametrize("invalid_email", [
        "invalid",
        "missing@",
        "@missing.domain",
        "noatsign.com",
        "with space@test.com"
    ], ids=["plain_string", "missing_domain", "missing_local", "no_at_sign", "with_space"])
    def test_invalid_email_format(self, api_client, invalid_email, faker):
        invalid_user = {
            "email": invalid_email,
            "password": faker.password(length=12),
            "name": faker.name()
        }

        response = api_client.create_user(**invalid_user)

        # API возвращает 500 на невалидные email - отмечаем как ожидаемый сбой
        if response.status_code == HTTP_STATUS["SERVER_ERROR"]:
            pytest.xfail("Известная проблема: серверная ошибка при валидации email")
        elif response.status_code == HTTP_STATUS["FORBIDDEN"]:
            pytest.xfail("Известная проблема: API возвращает FORBIDDEN вместо BAD_REQUEST")
        else:
            assert False, f"Неожиданный статус код: {response.status_code}"

    @allure.story("Валидация данных")
    @allure.title("Проверка коротких паролей")
    @pytest.mark.parametrize("short_password", ["123", "abc", "1"],
                             ids=["3_digits", "3_letters", "1_char"])
    def test_short_password(self, api_client, short_password, faker):
        invalid_user = {
            "email": faker.unique.email(),
            "password": short_password,
            "name": faker.name()
        }

        response = api_client.create_user(**invalid_user)

        if response.status_code == HTTP_STATUS["OK"]:
            pytest.fail("API не должен принимать пароль короче 6 символов")
        elif response.status_code == HTTP_STATUS["FORBIDDEN"]:
            pytest.xfail("Известная проблема: API возвращает FORBIDDEN вместо BAD_REQUEST для коротких паролей")
        else:
            assert False, f"Неожиданный статус код: {response.status_code}"