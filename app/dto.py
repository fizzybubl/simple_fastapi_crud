from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class ResponseDto(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserDto(BaseModel):
    email: EmailStr
    password: str


class UserResponseDto(ResponseDto):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data embedded into the JWT token."""
    id: Optional[int] = None


class Post(BaseModel):
    title: str
    content: str
    published: bool


class PostResponse(Post, ResponseDto):
    owner_id: int
    owner: UserResponseDto


class PostSchema(BaseModel):
    post: Post
    votes: int


class PostResponseSchema(BaseModel):
    PostEntity: PostResponse
    votes: int


class Vote(BaseModel):
    post_id: int
