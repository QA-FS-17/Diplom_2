# api_client.py

import requests
from urllib.parse import urljoin
import logging
from typing import Optional, Dict, Any

BASE_URL = "https://stellarburgers.nomoreparties.site/api/"

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class StellarBurgersApi:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}
        self.logger = logger

    def _request(self, method: str, endpoint: str,
                 json: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None) -> requests.Response:
        url = urljoin(self.base_url, endpoint)
        current_headers = self.headers.copy()
        if headers:
            current_headers.update(headers)

        self.logger.info(f"Request: {method} {url}")
        if json:
            self.logger.info(f"Request body: {json}")

        response = requests.request(method, url, json=json, headers=current_headers)

        self.logger.info(f"Response status: {response.status_code}")
        self.logger.info(f"Response body: {response.text}")

        return response

    # User methods
    def create_user(self, email: str = None, password: str = None, name: str = None) -> requests.Response:
        endpoint = "auth/register"
        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name
        return self._request("POST", endpoint, json=payload)

    def login_user(self, email: str, password: str) -> requests.Response:
        endpoint = "auth/login"
        payload = {
            "email": email,
            "password": password
        }
        return self._request("POST", endpoint, json=payload)

    def delete_user(self, access_token: str) -> requests.Response:
        if not access_token:
            raise ValueError("Access token is required")
        endpoint = "auth/user"
        headers = {"Authorization": access_token}
        return self._request("DELETE", endpoint, headers=headers)

    # Order methods
    def create_order(self, ingredients: list, access_token: Optional[str] = None) -> requests.Response:
        endpoint = "orders"
        headers = {}
        if access_token:
            headers["Authorization"] = access_token

        payload = {"ingredients": ingredients}
        return self._request("POST", endpoint, json=payload, headers=headers)

    def get_user_orders(self, access_token: Optional[str] = None) -> requests.Response:
        endpoint = "orders"
        headers = {}
        if access_token:
            headers["Authorization"] = access_token

        return self._request("GET", endpoint, headers=headers)

    # Profile methods
    def update_user_info(self, access_token=None, email=None, password=None, name=None):
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

    def get_user_info(self, access_token: str) -> requests.Response:
        if not access_token:
            raise ValueError("Access token is required")
        endpoint = "auth/user"
        headers = {"Authorization": access_token}
        return self._request("GET", endpoint, headers=headers)

    def get_ingredients(self) -> requests.Response:
        return self._request("GET", "ingredients")