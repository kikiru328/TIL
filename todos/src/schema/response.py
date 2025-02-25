from typing import List

from pydantic import BaseModel

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]
