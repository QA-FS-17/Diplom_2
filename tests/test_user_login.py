import allure
import pytest
from helpers.api_client import StellarBurgersApi
from helpers.data import TestUsers, HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.valid_user = TestUsers.VALID.copy()
        # Предварительная регистрация пользователя
        self.api.create_user(**self.valid_user)
        yield
        # Очистка данных
        login_response = self.api.login_user(self.valid_user["email"], self.valid_user["password"])
        if login_response.status_code == HTTP_STATUS["OK"]:
            token = login_response.json()["accessToken"]
            self.api.delete_user(token)

    @allure.story("Позитивные сценарии")
    @allure.title("Логин под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_existing_user(self):
        """Тест проверяет успешный логин с валидными кредами"""
        with allure.step("Отправка запроса на логин"):
            response = self.api.login_user(
                email=self.valid_user["email"],
                password=self.valid_user["password"]
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == HTTP_STATUS["OK"], "Неверный статус-код"
            response_data = response.json()
            assert response_data["success"] is True, "Флаг success не True"
            assert "accessToken" in response_data, "Нет accessToken в ответе"
            assert "refreshToken" in response_data, "Нет refreshToken в ответе"
            assert all(key in response_data["user"] for key in ["email", "name"]), "Некорректная структура user"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self):
        """Тест проверяет логин с некорректным паролем"""
        with allure.step("Отправка запроса с неверным паролем"):
            response = self.api.login_user(
                email=self.valid_user["email"],
                password="invalid_password"
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == HTTP_STATUS["UNAUTHORIZED"], "Неверный статус-код"
            assert response.json()["success"] is False, "Флаг success не False"
            assert response.json()["message"] == ERROR_MESSAGES["LOGIN_FAILED"], "Неверное сообщение об ошибке"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с несуществующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_email(self):
        """Тест проверяет логин с несуществующим email"""
        with allure.step("Отправка запроса с неверным email"):
            response = self.api.login_user(
                email="nonexistent@example.com",
                password=self.valid_user["password"]
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == HTTP_STATUS["UNAUTHORIZED"], "Неверный статус-код"
            assert response.json()["success"] is False, "Флаг success не False"
            assert response.json()["message"] == ERROR_MESSAGES["LOGIN_FAILED"], "Неверное сообщение об ошибке"