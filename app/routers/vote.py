from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app import dto
from app.models import VoteEntity
from app.oauth2 import get_current_user
from app.repository.vote_repo import VoteRepo, get_vote_repo
from app.services.vote_service import get_vote_service

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=HTTPStatus.CREATED)
def create_vote(vote_dto: dto.Vote, current_user=Depends(get_current_user),
                vote_service=Depends(get_vote_service)):
    vote_service.create_vote(post_id=vote_dto.post_id, user_id=current_user.id)
    return {"message": "successfully voted!"}


@router.delete("/", status_code=HTTPStatus.OK)
def delete_vote(vote_dto: dto.Vote, current_user=Depends(get_current_user),
                vote_service=Depends(get_vote_service)):
    vote_service.delete_vote(post_id=vote_dto.post_id, user_id=current_user.id)
    return {"message": "successfully removed vote!"}
