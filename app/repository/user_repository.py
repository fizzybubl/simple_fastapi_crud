from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserEntity
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):

    __entity_type__ = UserEntity

    def __init__(self, db: Session):
        super().__init__(db)

    def find_user_by_username(self, username: str):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.email == username).first()


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
