from http import HTTPStatus

import pytest

from tests.utils import get_token, random_input


@pytest.fixture(scope="session")
def create_user(client):
    def _create(payload, token):
        response = client.post("/users", json=payload, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == HTTPStatus.CREATED
        return response.json()
    return _create


def get_user_data():
    return {"email": f"dragos{random_input()}@gmail.com", "password": "12345"}


def test_create_user(client, access_token, create_user):
    user_data = get_user_data()
    create_user(user_data, access_token)
    get_token(client, user_data["email"], user_data["password"])


def test_get_user(client, access_token, create_user):
    user_data = get_user_data()
    user_response = create_user(user_data, access_token)
    token = get_token(client, user_data["email"], user_data["password"])
    user = client.get(f"/users/{user_response['id']}", headers={"Authorization": f"Bearer {token}"})
    assert user.status_code == HTTPStatus.OK
    assert user.json()["email"] == user_data["email"]


def test_delete_user(client, access_token, create_user):
    user_data = get_user_data()
    user_response = create_user(user_data, access_token)
    token = get_token(client, user_data["email"], user_data["password"])
    response = client.delete(f"/users/{user_response['id']}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT
