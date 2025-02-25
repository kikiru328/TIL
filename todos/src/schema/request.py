from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    """
    Create Request Body (Format)
    id: int #auto increment
    """

    contents: str
    is_done: bool
