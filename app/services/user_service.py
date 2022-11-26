from fastapi import Depends

from app import dto, models
from app.repository.user_repository import UserRepository, get_user_repo
from app.utils import hash_password


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: dto.UserDto):
        user.password = hash_password(user.password)
        return self.user_repo.save(models.UserEntity(**user.dict()))

    def get_user_by_id(self, id_: int):
        return self.user_repo.find_by_id(id_)

    def delete_user(self, id_: int):
        self.user_repo.delete_by_id(id_)


def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo)
