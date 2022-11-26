from http import HTTPStatus

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import dto
from app.database import get_db
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=dto.UserResponseDto)
def create_user(user: dto.UserDto, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user_dto=user)


@router.get("/{id_}", response_model=dto.UserResponseDto)
def get_user(id_: int, db: Session = Depends(get_db)):
    return user_service.get_user(db=db, user_id=id_)


@router.delete("/{id_}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(id_: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db=db, user_id=id_)
