from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ResponseSchema(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBody(BaseModel):
    email: EmailStr
    password: str


class UserResponse(ResponseSchema):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data embedded into the JWT token."""
    id: Optional[int] = None


class PostBody(BaseModel):
    title: str
    content: str
    published: bool


class PostResponse(PostBody, ResponseSchema):
    owner_id: int


class PostSchema(BaseModel):
    post: PostBody
    votes: Optional[int] = 0


class PostResponseSchema(BaseModel):
    PostEntity: PostResponse
    votes: Optional[int] = 0

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
