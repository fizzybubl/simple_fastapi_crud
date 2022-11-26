from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import VoteEntity
from app.repository.base_repository import BaseRepository


class VoteRepo(BaseRepository):
    __entity_type__ = VoteEntity

    def __init__(self, db: Session):
        super(VoteRepo, self).__init__(db)

    def find_by_id(self, post_id: int, user_id: int):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.post_id == post_id,
                                                          self.__entity_type__.user_id == user_id).first()

    def delete_by_id(self, post_id: int, user_id: int):
        self.db.query(self.__entity_type__).filter(self.__entity_type__.post_id == post_id,
                                                   self.__entity_type__.user_id == user_id).delete()
        self.db.commit()
        return


def get_vote_repo(db: Session = Depends(get_db)):
    return VoteRepo(db)
