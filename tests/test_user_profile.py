import allure
from helpers.data import HTTP_STATUS, ERROR_MESSAGES


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUserProfile:
    # С авторизацией
    @allure.story("Авторизованный пользователь")
    @allure.title("Изменение имени пользователя")
    def test_update_name_authorized(self, api_client, registered_user):
        new_name = "Новое Имя"
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            name=new_name
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["user"]["name"] == new_name

    @allure.story("Авторизованный пользователь")
    @allure.title("Изменение email пользователя")
    def test_update_email_authorized(self, api_client, registered_user):
        new_email = "new_email@example.com"
        response = api_client.update_user_info(
            access_token=registered_user["access_token"],
            email=new_email
        )
        assert response.status_code == HTTP_STATUS["OK"]
        assert response.json()["user"]["email"] == new_email


    # Без авторизации
    @allure.story("Неавторизованный пользователь")
    @allure.title("Попытка изменения данных без авторизации")
    def test_update_unauthorized(self, api_client):
        response = api_client.update_user_info(name="Новое Имя")
        assert response.status_code == HTTP_STATUS["UNAUTHORIZED"]
        assert response.json()["message"] == ERROR_MESSAGES["UNAUTHORIZED"]