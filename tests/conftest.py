import pytest
from helpers.api_client import StellarBurgersApi
from helpers.data import TestUsers

@pytest.fixture
def api_client():
    return StellarBurgersApi()

@pytest.fixture
def registered_user(api_client):
    """Фикстура с зарегистрированным пользователем"""
    response = api_client.create_user(**TestUsers.VALID)
    yield {
        **TestUsers.VALID,
        "access_token": response.json()["accessToken"]
    }
    # Пост-очистка
    api_client.delete_user(response.json()["accessToken"])