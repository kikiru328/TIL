from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    """
    Create Request Body (Format)
    id: increment
    """
    contents: str
    is_done: bool