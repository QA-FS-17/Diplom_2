import requests
from urllib.parse import urljoin

BASE_URL = "https://stellarburgers.nomoreparties.site/api/"

class StellarBurgersApi:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}

    def _request(self, method, endpoint, json=None, headers=None):
        url = urljoin(self.base_url, endpoint)
        current_headers = self.headers.copy()
        if headers:
            current_headers.update(headers)
        return requests.request(method, url, json=json, headers=current_headers)

    # User methods
    def create_user(self, email, password, name):
        """Регистрация нового пользователя"""
        endpoint = "auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return self._request("POST", endpoint, json=payload)

    def login_user(self, email, password):
        """Авторизация пользователя"""
        endpoint = "auth/login"
        payload = {
            "email": email,
            "password": password
        }
        return self._request("POST", endpoint, json=payload)

    def delete_user(self, access_token):
        """Удаление пользователя"""
        endpoint = "auth/user"
        headers = {"Authorization": access_token}
        return self._request("DELETE", endpoint, headers=headers)

    # Order methods
    def create_order(self, ingredients, access_token=None):
        """Создание заказа"""
        endpoint = "orders"
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        payload = {"ingredients": ingredients}
        return self._request("POST", endpoint, json=payload, headers=headers)

    def get_user_orders(self, access_token=None):
        """Получение заказов пользователя"""
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        return self._request("GET", "orders", headers=headers)

    # Profile methods
    def update_user_info(self, access_token=None, email=None, password=None, name=None):
        """Обновление данных пользователя"""
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        payload = {}
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        if name:
            payload["name"] = name
        return self._request("PATCH", "auth/user", json=payload, headers=headers)

    def get_user_info(self, access_token):
        """Получение информации о пользователе"""
        endpoint = "auth/user"
        headers = {"Authorization": access_token}
        return self._request("GET", endpoint, headers=headers)