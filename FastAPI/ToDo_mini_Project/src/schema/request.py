from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    """
    Create Request Body (Format)
    id: increment
    """
    contents: str
    is_done: bool

class SignUpRequest(BaseModel):
    username: str
    password: str

class LogInRequest(BaseModel):
    username: str
    password: str

class CreateOTPRequest(BaseModel):
    email: str