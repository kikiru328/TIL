from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True # sqlalchemy orm 객체 자동 변환

class JWTSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PostSchema(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class LikeSchema(BaseModel):
    post_id: int
    user_id: Optional[int]
    message: Optional[str]
    like_count: int

class CommentSchema(BaseModel):
    id: int # comment id
    post_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True