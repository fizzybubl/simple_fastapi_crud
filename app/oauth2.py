from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app import dto
from app.config import settings
from app.repository.user_repository import UserRepository, get_user_repo


oauth_schema = OAuth2PasswordBearer(tokenUrl="authenticate")


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.token_timeout)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_access_token(token: str, exc: Exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id_ = payload.get("user_id")
        if not id_:
            raise exc
        return dto.TokenData(id=id_)
    except JWTError:
        raise exc


def get_current_user(token: str = Depends(oauth_schema), user_repo: UserRepository = Depends(get_user_repo)):
    credentials_exception = HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token=token, exc=credentials_exception)
    return user_repo.find_by_id(token.id)

