from http import HTTPStatus

from fastapi import Depends, APIRouter

from app import dto
from app.services.user_service import UserService, get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=dto.UserResponseDto)
def create_user(user: dto.UserDto, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)


@router.get("/{id_}", response_model=dto.UserResponseDto)
def get_user(id_: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(id_)


@router.delete("/{id_}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(id_: int, user_service: UserService = Depends(get_user_service)):
    return user_service.delete_user(id_)
