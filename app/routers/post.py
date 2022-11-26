from http import HTTPStatus
from typing import Optional

from fastapi import Depends, APIRouter

from app import dto
from app.models import UserEntity
from app.oauth2 import get_current_user
from app.services.post_service import get_post_service, PostService

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[dto.PostResponseDto])
def get_posts(post_service: PostService = Depends(get_post_service),
              current_user: UserEntity = Depends(get_current_user),
              limit: int = 5,
              skip: int = 0,
              search: Optional[str] = ""):
    return post_service.get_posts(limit, skip)


@router.get("/{id_}", response_model=dto.PostResponseDto)
def get_post(id_: int, post_service: PostService = Depends(get_post_service),
             current_user: UserEntity = Depends(get_current_user)):
    return post_service.get_post(id_=id_)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=dto.PostResponseDto)
def create_posts(post: dto.PostDto,
                 post_service: PostService = Depends(get_post_service),
                 current_user: UserEntity = Depends(get_current_user)):
    return post_service.create_post(post, owner_id=current_user.id)


@router.delete("/{id_}", status_code=HTTPStatus.NO_CONTENT)
def delete_post(id_: int,
                post_service: PostService = Depends(get_post_service),
                current_user=Depends(get_current_user)):
    return post_service.delete_post(id_, current_user.id)


@router.put("/{id_}", status_code=HTTPStatus.OK)
def update_post(id_: int,
                post: dto.PostDto,
                post_service: PostService = Depends(get_post_service),
                current_user=Depends(get_current_user)):
    return post_service.update_post(id_=id_, post_dto=post, owner_id=current_user.id)
