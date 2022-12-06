from http import HTTPStatus

import pytest


@pytest.fixture(scope="session")
def create_post(client):
    def _create(payload, access_token):
        response = client.post("/posts", headers={"Authorization": f"Bearer {access_token}"}, json=payload)
        assert response.status_code == HTTPStatus.CREATED
        return response.json()
    return _create


def test_get_posts(client, access_token):
    posts = client.get("/posts", headers={"Authorization": f"Bearer {access_token}"})
    assert posts.status_code == HTTPStatus.OK
    assert len(posts.json()) > 0


def test_get_post_by_id(client, access_token, create_post):
    post_payload = {
        "title": "Book Title",
        "content": "Book Content",
        "published": False
    }
    created_post = create_post(post_payload, access_token)
    response = client.get(f"/posts/{created_post['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["PostEntity"]
    assert response_json["title"] == post_payload["title"]
    assert response_json["content"] == post_payload["content"]
    assert response_json["published"] == post_payload["published"]


def test_create_post(create_post, access_token):
    post_payload = {
        "title": "Book Title",
        "content": "Book Content",
        "published": False
    }
    created_post = create_post(post_payload, access_token)
    assert created_post["title"] == post_payload["title"]
    assert created_post["content"] == post_payload["content"]
    assert created_post["published"] == post_payload["published"]


def test_update_post(client, access_token):
    post_payload = {
        "title": "Book Title",
        "content": "Book Content",
        "published": False
    }
    created_post = create_post(post_payload, access_token)
    update_payload = {
        "title": "Book Title Updated",
        "content": "Book Content Updated",
        "published": True
    }
    response = client.put(f"/posts/{created_post['id']}",
                          headers={"Authorization": f"Bearer {access_token}"},
                          json=update_payload)
    assert response.status_code == HTTPStatus.OK
    response = client.get(f"/posts/{created_post['id']}",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["PostEntity"]
    assert response_json["title"] == update_payload["title"]
    assert response_json["content"] == update_payload["content"]
    assert response_json["published"] == update_payload["published"]


def test_delete_post(client, access_token):
    post_payload = {
        "title": "Book Title",
        "content": "Book Content",
        "published": False
    }
    created_post = create_post(post_payload, access_token)
    response = client.delete(f"/posts/{created_post['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT
