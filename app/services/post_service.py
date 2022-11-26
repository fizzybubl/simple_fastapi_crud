from http import HTTPStatus

from fastapi import HTTPException, Depends

from app import dto, models
from app.repository.post_repository import PostRepository, get_post_repo


class PostService:

    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def verify_owner(self, post_owner_id, user_id):
        if post_owner_id != user_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")

    def get_posts(self, limit=5, skip=0):
        return self.post_repo.find_all(limit, skip)

    def get_post(self, id_: int):
        post = self.post_repo.find_by_id(id_)
        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post with id {id_} was not found")
        return post

    def create_post(self, post: dto.PostDto, owner_id: int):
        return self.post_repo.save(models.PostEntity(owner_id=owner_id, **post.dict()))

    def delete_post(self, id_: int, owner_id: int):
        post = self.post_repo.find_by_id(id_)
        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post with id {id_} was not found")
        self.verify_owner(post.owner_id, owner_id)
        return self.post_repo.delete_by_id(id_)

    def update_post(self, id_: int, post_dto: dto.PostDto, owner_id):
        post = self.post_repo.find_by_id(id_)
        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post with id {id_} was not found")
        self.verify_owner(post.owner_id, owner_id)
        return self.post_repo.update(new_values=post_dto.dict(), id_=id_)


def get_post_service(post_repo: PostRepository = Depends(get_post_repo)):
    return PostService(post_repo)
