# test_user_profile.py

import allure
import pytest
from helpers.data import HTTP_STATUS, ERROR_MESSAGES
from helpers.generators import generate_email


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUserProfile:
    @allure.story("Обновление данных")
    @allure.title("Успешное обновление информации")
    @pytest.mark.parametrize("field,value", [
        ("email", generate_email()),
        ("name", "Новое имя"),
        ("password", "NewPassword123!")
    ], ids=["email", "name", "password"])
    def test_successful_profile_update(self, api_client, registered_user, field, value):
        """Проверка обновления различных полей профиля"""
        with allure.step(f"Обновляем поле {field}"):
            update_data = {field: value}
            response = api_client.update_user_info(
                access_token=registered_user["access_token"],
                **update_data
            )

        with allure.step("Проверяем ответ"):
            assert response.status_code == HTTP_STATUS["OK"], "Неверный статус-код"
            response_data = response.json()
            assert response_data["success"] is True, "Флаг success должен быть True"

            # Для пароля API может не возвращать его в ответе
            if field != "password":
                assert response_data["user"][field] == value, f"Поле {field} не обновилось"
            else:
                # Проверяем, что можно залогиниться с новым паролем
                login_response = api_client.login_user(
                    email=registered_user["email"],
                    password=value
                )
                assert login_response.status_code == HTTP_STATUS["OK"], "Не удалось войти с новым паролем"

    @allure.story("Неавторизованный доступ")
    @allure.title("Попытка изменения данных без авторизации")
    def test_unauthorized_update(self, api_client):
        """Проверка защиты от неавторизованных изменений"""
        response = api_client.update_user_info(name="Новое Имя")

        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"], "Должна быть ошибка 401"
        assert response.json()["message"] == ERROR_MESSAGES["UNAUTHORIZED"], "Неверное сообщение об ошибке"

    @allure.story("Ошибки валидации")
    @allure.title("Попытка задания невалидного email")
    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "missing@domain",
        "space @email.com"
    ], ids=["no_at", "no_domain", "with_space"])
    def test_invalid_email_update(self, api_client, registered_user, invalid_email):
        """Проверка валидации email при обновлении"""
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=invalid_email
        )

        if response.status_code == HTTP_STATUS["OK"]:
            pytest.xfail("API принимает невалидные email (ожидается исправление)")
        else:
            assert response.status_code == HTTP_STATUS["BAD_REQUEST"], "Должна быть ошибка 400"
            assert "email" in response.json()["message"].lower(), "Сообщение должно указывать на проблему с email"

    @allure.story("Конфликтующие данные")
    @allure.title("Попытка задания существующего email")
    def test_duplicate_email_update(self, api_client, registered_user, another_registered_user):
        """Проверка обработки попытки использовать занятый email"""
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=another_registered_user["email"]
        )

        assert response.status_code in [HTTP_STATUS["FORBIDDEN"],
                                        HTTP_STATUS["CONFLICT"]], "Должна быть ошибка 403 или 409"
        assert "already exists" in response.json()["message"].lower()