from http import HTTPStatus

from tests.utils import get_post_payload


def test_add_vote(client, create_post, access_token):
    post = create_post(get_post_payload(), access_token)
    response = client.put(f"/votes/{post['id']}",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == HTTPStatus.OK
    post_response = client.get(f"/posts/{post['id']}", headers={"Authorization": f"Bearer {access_token}"}).json()
    assert post_response["votes"] == 1


def test_remove_vote(client, access_token, create_post):
    post = create_post(get_post_payload(), access_token)
    client.post("/votes",
                headers={"Authorization": f"Bearer {access_token}"},
                json={"post_id": post['id']})
    client.delete(f"/votes/{post['id']}",
                  headers={"Authorization": f"Bearer {access_token}"})
    post_response = client.get(f"/posts/{post['id']}", headers={"Authorization": f"Bearer {access_token}"}).json()
    assert post_response["votes"] == 0
