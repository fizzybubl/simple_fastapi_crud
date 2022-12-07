from http import HTTPStatus
from typing import Optional

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import UserEntity
from app.oauth2 import get_current_user
from app.services import post_service

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              current_user: UserEntity = Depends(get_current_user),
              limit: int = 5,
              skip: int = 0,
              search: Optional[str] = ""):
    return post_service.get_posts(db=db, limit=limit, offset=skip)


@router.get("/{id_}", response_model=schemas.PostResponseSchema)
def get_post(id_: int, db: Session = Depends(get_db),
             current_user: UserEntity = Depends(get_current_user)):
    return post_service.get_post(db=db, post_id=id_)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostBody,
                db: Session = Depends(get_db),
                current_user: UserEntity = Depends(get_current_user)):
    return post_service.create_post(db=db, post_dto=post, owner_id=current_user.id)


@router.delete("/{id_}", status_code=HTTPStatus.NO_CONTENT)
def delete_post(id_: int,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    return post_service.delete_post(db=db, post_id=id_, user_id=current_user.id)


@router.put("/{id_}", status_code=HTTPStatus.OK)
def update_post(id_: int,
                post: schemas.PostBody,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    return post_service.update_post(db=db, post_id=id_, user_id=current_user.id, post_dto=post)
