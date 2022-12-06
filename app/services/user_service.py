from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import dto
from app.models import UserEntity
from app.utils import hash_password


def create_user(db: Session, user_dto: dto.UserDto):
    user_dto.password = hash_password(user_dto.password)
    new_user = UserEntity(**user_dto.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"User with id {user_id} not found!")
    return user


def delete_user(db: Session, user_id):
    user_query = db.query(UserEntity).filter(UserEntity.id == user_id)
    if not user_query.first():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"User with id {user_id} not found!")
    return user_query.delete()
