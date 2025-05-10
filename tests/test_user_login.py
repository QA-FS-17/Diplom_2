import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:
    # Позитивные проверки
    @allure.story("Успешный логин")
    @allure.title("Код ответа 200 при валидных данных")
    def test_login_status_code(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert response.status_code == HTTP_STATUS["OK"]

    @allure.story("Успешный логин")
    @allure.title("Флаг success=True при валидных данных")
    def test_login_success_flag(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert response.json()["success"] is True

    @allure.story("Успешный логин")
    @allure.title("Наличие accessToken в ответе")
    def test_login_has_access_token(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert "accessToken" in response.json()

    @allure.story("Успешный логин")
    @allure.title("Наличие refreshToken в ответе")
    def test_login_has_refresh_token(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
        assert "refreshToken" in response.json()


    # Негативные проверки
    @allure.story("Неверные данные")
    @allure.title("Код 401 при неверном пароле")
    def test_wrong_password_status(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password="invalid_password"
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    @allure.story("Неверные данные")
    @allure.title("Сообщение об ошибке при неверном пароле")
    def test_wrong_password_message(self, api_client, registered_user):
        response = api_client.login_user(
            email=registered_user["email"],
            password="invalid_password"
        )
        assert response.json()["message"] == ERROR_MESSAGES["LOGIN_FAILED"]

    @allure.story("Неверные данные")
    @allure.title("Код 401 при несуществующем email")
    def test_nonexistent_email_status(self, api_client, registered_user):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password=registered_user["password"]
        )
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]

    @allure.story("Неверные данные")
    @allure.title("Флаг success=False при неверных данных")
    def test_invalid_credentials_success_flag(self, api_client):
        response = api_client.login_user(
            email="nonexistent@example.com",
            password="invalid_password"
        )
        assert response.json()["success"] is False