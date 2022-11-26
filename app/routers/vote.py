from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dto
from app.database import get_db
from app.oauth2 import get_current_user
from app.services import vote_service

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=HTTPStatus.CREATED)
def create_vote(vote_dto: dto.Vote, current_user=Depends(get_current_user),
                db: Session = Depends(get_db)):
    vote_service.create_vote(db=db, post_id=vote_dto.post_id, user_id=current_user.id)
    return {"message": "successfully voted!"}


@router.delete("/", status_code=HTTPStatus.OK)
def delete_vote(vote_dto: dto.Vote, current_user=Depends(get_current_user),
                db: Session = Depends(get_db)):
    vote_service.delete_vote(db=db, post_id=vote_dto.post_id, user_id=current_user.id)
    return {"message": "successfully removed vote!"}
