from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import utils, oauth2, dto
from app.repository.user_repository import get_user_repo, UserRepository

router = APIRouter(tags=["Authentication"])


@router.post("/authenticate", response_model=dto.Token)
def authenticate(user_credentials: OAuth2PasswordRequestForm = Depends(),
                 user_repo: UserRepository = Depends(get_user_repo)):
    user = user_repo.find_user_by_username(user_credentials.username)
    if not user:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"Invalid credentials!")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"Invalid credentials!")

    access_token = oauth2.generate_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
