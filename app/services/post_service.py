from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, Query

from app.dto import Post
from app.models import PostEntity, VoteEntity


def get_posts(db: Session, limit: int = 5, offset: int = 0):
    return db.query(PostEntity, func.count(VoteEntity.post_id).label("votes")) \
        .join(VoteEntity, PostEntity.id == VoteEntity.post_id, isouter=True) \
        .group_by(PostEntity.id).limit(limit).offset(offset).all()


def get_post(db: Session, post_id: int):
    post = db.query(PostEntity, func.count(VoteEntity.post_id).label("votes")) \
        .join(VoteEntity, PostEntity.id == VoteEntity.post_id, isouter=True) \
        .group_by(PostEntity.id)\
        .filter(PostEntity.id == post_id)\
        .first()
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post with id {post_id} was not found")
    return post


def create_post(db: Session, post_dto: Post, owner_id: int):
    new_post = PostEntity(owner_id=owner_id, **post_dto.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def _check_post_existence(post_query: Query, post_id):
    if not post_query.first():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post with id {post_id} was not found")


def _check_owner_id(post_query: Query, user_id):
    if post_query.first().owner_id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")


def update_post(db: Session, post_id: int, post_dto: Post, user_id: int):
    post_query = db.query(PostEntity).filter(PostEntity.id == post_id)
    _check_post_existence(post_query, post_id)
    _check_owner_id(post_query, user_id)
    post_query.update(post_dto.dict())
    db.commit()
    return True


def delete_post(db: Session, post_id: int, user_id: int):
    post_query = db.query(PostEntity).filter(PostEntity.id == post_id)
    _check_post_existence(post_query, post_id)
    _check_owner_id(post_query, user_id)
    post_query.delete()
    db.commit()
    return
