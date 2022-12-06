from http import HTTPStatus

from tests.utils import get_post_payload


def test_get_posts(client, access_token):
    posts = client.get("/posts", headers={"Authorization": f"Bearer {access_token}"})
    assert posts.status_code == HTTPStatus.OK
    assert len(posts.json()) > 0


def test_get_post_by_id(client, access_token, create_post):
    post_payload = get_post_payload()
    created_post = create_post(post_payload, access_token)
    response = client.get(f"/posts/{created_post['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["PostEntity"]
    assert_equals(post_payload, response_json)


def test_create_post(create_post, access_token):
    post_payload = get_post_payload()
    created_post = create_post(post_payload, access_token)
    assert_equals(post_payload, created_post)


def test_update_post(client, access_token, create_post):
    post_payload = get_post_payload()
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
    assert_equals(update_payload, response_json)


def test_delete_post(client, access_token, create_post):
    post_payload = get_post_payload()
    created_post = create_post(post_payload, access_token)
    response = client.delete(f"/posts/{created_post['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT


def assert_equals(expected, actual):
    assert actual["title"] == expected["title"]
    assert actual["content"] == expected["content"]
    assert actual["published"] == expected["published"]
