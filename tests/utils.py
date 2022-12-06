from http import HTTPStatus
from random import random


def get_token(client, username, password):
    response = client.post("/authenticate",
                           data={"username": username, "password": password})
    assert response.status_code == HTTPStatus.OK
    return response.json()["access_token"]


def random_input():
    return random() * 10_000_000


def get_post_payload():
    return {
        "title": f"Book Title {random_input()}",
        "content": "Book Content",
        "published": False
    }