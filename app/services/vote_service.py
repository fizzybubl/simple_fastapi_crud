from http import HTTPStatus

from fastapi import Depends, HTTPException

from app.models import VoteEntity
from app.repository.post_repository import PostRepository, get_post_repo
from app.repository.vote_repo import VoteRepo, get_vote_repo


class VoteService:

    def __init__(self, vote_repo: VoteRepo, post_repo: PostRepository):
        self.vote_repo = vote_repo
        self.post_repo = post_repo

    def check_if_post_exists(self, post_id):
        if not self.post_repo.find_by_id(post_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post {post_id} does not exist!")

    def create_vote(self, post_id, user_id):
        self.check_if_post_exists(post_id)
        if self.vote_repo.find_by_id(post_id, user_id):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f"User {user_id} has already voted on"
                                                                        f"post {post_id}")
        return self.vote_repo.save(VoteEntity(post_id=post_id, user_id=user_id))

    def delete_vote(self, post_id, user_id):
        self.check_if_post_exists(post_id)
        if not self.vote_repo.find_by_id(post_id, user_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Vote does not exist!")
        return self.vote_repo.delete_by_id(post_id=post_id, user_id=user_id)


def get_vote_service(vote_repo=Depends(get_vote_repo), post_repo=Depends(get_post_repo)):
    return VoteService(vote_repo, post_repo)
