from typing import List

from fastapi import Depends, HTTPException, Body, APIRouter
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

router = APIRouter(prefix="/todos") # Connect API with main & prefix todos

@router.get("", status_code=200) # 200: OK
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db)
) -> ToDoListSchema:
    """
    Get all data from the database according to the specified order.
    The order is requested based on the query.
    e.g., "/todos?order=DESC"
    """
    todos: List[ToDo] = get_todos(session=session) # from db
    if order and order == "DESC": #decending
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    #return todos #default == ascending
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/{todo_id}", status_code=200)
def get_todo_by_todo_id_handler(
        todo_id: int,
        session: Session = Depends(get_db)
) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")
    #return todo_data.get(todo_id, {}) # else: return blank dict


@router.post("", status_code=201) # create
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db),
) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo) # id:int

    #todo_data[request.id] = request.dict() # BaseModel Method
    #return todo_data[request.id]
    return ToDoSchema.from_orm(todo)


@router.patch("/{todo_id}", status_code=200) # OK
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db), #request body 중 하나만 전달
):

    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.delete("/{todo_id}", status_code=204) # No Content
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    delete_todo(session=session, todo_id=todo_id)
