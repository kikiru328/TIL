from pydantic import BaseModel


class SignUpRequest(BaseModel):
    username: str
    password: str

class LogInRequest(BaseModel):
    username: str
    password: str

class PostRequest(BaseModel):
    content: str

class LikeRequest(BaseModel):
    post_id: int

class CommentRequest(BaseModel):
    content: str