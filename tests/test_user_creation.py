import allure
import pytest
from helpers.api_client import StellarBurgersApi
from helpers.data import TestUsers, HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.valid_user = TestUsers.VALID.copy()  # Копируем, чтобы не модифицировать оригинал
        yield
        # Пост-очистка
        if hasattr(self, 'access_token'):
            self.api.delete_user(self.access_token)

    @allure.story("Позитивные сценарии")
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_unique_user(self):
        """
        Тест проверяет успешную регистрацию нового пользователя
        с валидными данными
        """
        with allure.step("Отправка запроса на регистрацию"):
            response = self.api.create_user(**self.valid_user)

        with allure.step("Проверка ответа"):
            assert response.status_code == HTTP_STATUS["OK"], "Неверный статус-код"
            assert response.json()["success"] is True, "Флаг success не True"
            assert "accessToken" in response.json(), "Нет токена в ответе"
            self.access_token = response.json()["accessToken"]

    @allure.story("Негативные сценарии")
    @allure.title("Попытка создать уже зарегистрированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self):
        """
        Тест проверяет обработку попытки регистрации пользователя,
        который уже существует в системе
        """
        with allure.step("Первичная регистрация пользователя"):
            self.api.create_user(**self.valid_user)

        with allure.step("Повторная регистрация с теми же данными"):
            response = self.api.create_user(**self.valid_user)

        with allure.step("Проверка ошибки"):
            assert response.status_code == HTTP_STATUS["FORBIDDEN"], "Неверный статус-код"
            assert response.json()["message"] == ERROR_MESSAGES["USER_EXISTS"], "Неверное сообщение об ошибке"

    @allure.story("Негативные сценарии")
    @allure.title("Создание пользователя без обязательного поля: {field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("field", ["email", "password", "name"],
                             ids=["без email", "без пароля", "без имени"])
    def test_missing_required_field(self, field):
        """
        Тест проверяет обработку отсутствия обязательных полей
        при регистрации пользователя
        """
        test_user = self.valid_user.copy()
        test_user.pop(field)  # Удаляем одно поле

        with allure.step(f"Отправка запроса без поля '{field}'"):
            response = self.api.create_user(**test_user)

        with allure.step("Проверка ответа"):
            assert response.status_code == HTTP_STATUS["FORBIDDEN"], "Неверный статус-код"
            assert ERROR_MESSAGES["REQUIRED_FIELDS"] in response.json()["message"], "Неверное сообщение об ошибке"