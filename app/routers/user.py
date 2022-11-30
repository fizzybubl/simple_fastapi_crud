from http import HTTPStatus

from fastapi import APIRouter

from app import dto
from app.database import session_factory
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=dto.UserResponseDto)
def create_user(user: dto.UserDto):
    with session_factory() as session:
        return user_service.create_user(db=session, user_dto=user)


@router.get("/{id_}", response_model=dto.UserResponseDto)
def get_user(id_: int):
    with session_factory() as session:
        return user_service.get_user(db=session, user_id=id_)


@router.delete("/{id_}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(id_: int):
    with session_factory() as session:
        return user_service.delete_user(db=session, user_id=id_)
