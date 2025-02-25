from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    """
    Create Request Body (Format)
    """
    id: int
    contents: str
    is_done: bool
