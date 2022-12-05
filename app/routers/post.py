from http import HTTPStatus
from typing import Optional

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import dto
from app.database import session_factory
from app.models import UserEntity
from app.oauth2 import get_current_user
from app.services import post_service

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


def use_session(_func=None):
    print(_func)
    def outer(func):
        print(func)

        def inner(*args, **kwargs):
            with session_factory() as session:
                print("generated session")
                args = [*args, session]
                r = func(*args, **kwargs)
                return r

        print(func)
        return inner

    return outer(_func) if _func else outer


@router.get("/")
def get_posts(current_user: UserEntity = Depends(get_current_user),
              limit: int = 5,
              skip: int = 0,
              search: Optional[str] = ""):
    with session_factory() as session:
        return post_service.get_posts(db=session, limit=limit, offset=skip)


@router.get("/{id_}", response_model=dto.PostResponseSchema)
def get_post(id_: int, current_user: UserEntity = Depends(get_current_user)):
    with session_factory() as session:
        return post_service.get_post(db=session, post_id=id_)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=dto.PostResponseSchema)
def create_posts(post: dto.PostSchema, current_user: UserEntity = Depends(get_current_user)):
    with session_factory() as session:
        return post_service.create_post(db=session, post_dto=post, owner_id=current_user.id)


@router.delete("/{id_}", status_code=HTTPStatus.NO_CONTENT)
def delete_post(id_: int,
                current_user=Depends(get_current_user)):
    with session_factory() as session:
        return post_service.delete_post(db=session, post_id=id_, user_id=current_user.id)


@router.put("/{id_}", status_code=HTTPStatus.OK)
def update_post(id_: int,
                post: dto.PostSchema,
                current_user=Depends(get_current_user)):
    with session_factory() as session:
        return post_service.update_post(db=session, post_id=id_, user_id=current_user.id, post_dto=post)
