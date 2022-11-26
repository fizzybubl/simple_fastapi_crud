from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import VoteEntity, PostEntity


def create_vote(db: Session, user_id, post_id):
    if not db.query(PostEntity).filter(PostEntity.id == post_id).first():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Post {post_id} does not exist!")
    if db.query(VoteEntity).filter(VoteEntity.user_id == user_id, VoteEntity.post_id == post_id).first():
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f"User {user_id} has already voted on"
                                                                    f"post {post_id}")
    db.add(VoteEntity(user_id=user_id, post_id=post_id))
    db.commit()
    return True


def delete_vote(db: Session, user_id, post_id):
    post_query = db.query(VoteEntity).filter(VoteEntity.user_id == user_id, VoteEntity.post_id == post_id)
    if not post_query.first():
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f"Vote does not exist!")
    post_query.delete()
    db.commit()
    return True
