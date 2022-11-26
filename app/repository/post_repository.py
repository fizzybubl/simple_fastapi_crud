from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PostEntity
from app.repository.base_repository import BaseRepository


class PostRepository(BaseRepository):
    __entity_type__ = PostEntity

    def __init__(self, db: Session):
        super().__init__(db)

    def find_all_by_owner_id(self, owner_id):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.owner_id == owner_id).all()


def get_post_repo(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)
