from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import utils, oauth2, schemas
from app.database import get_db
from app.models import UserEntity

router = APIRouter(tags=["Authentication"])


@router.post("/authenticate", response_model=schemas.Token)
def authenticate(user_credentials: OAuth2PasswordRequestForm = Depends(),
                 db: Session = Depends(get_db)):
    user = db.query(UserEntity).filter(UserEntity.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"Invalid credentials!")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"Invalid credentials!")

    access_token = oauth2.generate_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
