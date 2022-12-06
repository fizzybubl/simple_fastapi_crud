from http import HTTPStatus
from random import random

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.config import settings
from app.database import get_db, BaseEntity
from app.main import app

_TESTING_DB_CONNECTION_STRING = f"mysql+pymysql://{settings.database_user}:{settings.database_password}" \
                                f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(_TESTING_DB_CONNECTION_STRING)  # creates DB connection
testing_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # DB session for transactions
BaseEntity.metadata.create_all(bind=engine)


def get_testing_db():
    db = testing_session_factory()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def db_client():
    return get_testing_db()


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = get_testing_db
    yield TestClient(app)


@pytest.fixture()
def access_token(client):
    response = client.post("/authenticate",
                           data={"username": "daniil@gmail.com", "password": "12345"})
    assert response.status_code == HTTPStatus.OK
    return response.json()["access_token"]


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


@pytest.fixture(scope="session")
def create_post(client):
    def _create(payload, access_token):
        response = client.post("/posts", headers={"Authorization": f"Bearer {access_token}"}, json=payload)
        assert response.status_code == HTTPStatus.CREATED
        return response.json()
    return _create