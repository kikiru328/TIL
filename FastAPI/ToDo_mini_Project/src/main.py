# framework
from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()

# API: Get method
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

# Temporary Database
todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": False,
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    }
}

# API: Get Method 2,
@app.get("/todos", status_code=200) # 200: OK
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
    #return todos
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

# API: Get Method 3,
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_by_todo_id_handler(
        todo_id: int,
        session: Session = Depends(get_db)
) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found") #no todo id

# API: Post Method
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db),
) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo) # id:int

    #todo_data[request.id] = request.dict() # BaseModel Method
    #return todo_data[request.id]
    return ToDoSchema.from_orm(todo)

# API: Patch Method
@app.patch("/todos/{todo_id}", status_code=200) # OK
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

# API: Delete Method
@app.delete("/todos/{todo_id}", status_code=204) # No Content
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
):
    #todo = todo_data.pop(todo_id, None)
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    delete_todo(session=session, todo_id=todo_id)