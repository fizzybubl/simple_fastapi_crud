from sqlalchemy.orm import Session

from app.database import BaseEntity


class BaseRepository:

    __entity_type__ = BaseEntity

    def __init__(self, db: Session):
        self.db = db

    def save(self, entity) -> __entity_type__:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def find_by_id(self, id_) -> __entity_type__:
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).first()

    def find_all(self, limit, skip):
        return self.db.query(self.__entity_type__).limit(limit).offset(skip).all()

    def delete_by_id(self, id_):
        self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).delete()
        self.db.commit()
        return

    def update(self, new_values, id_):
        self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).update(new_values)
        self.db.commit()
        return True
