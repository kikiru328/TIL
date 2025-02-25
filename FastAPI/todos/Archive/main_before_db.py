#  framework
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()

# DB
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

# API: Get Method 1
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

# API: Get Method 2,
@app.get("/todos", status_code=200) # 200: OK
def get_todos_handler(order: str | None = None) -> list:
    """
    Get all data from the database according to the specified order.
    The order is requested based on the query.
    e.g., "/todos?order=DESC"
    """
    ret = list(todo_data.values())
    if order and order == "DESC": #decending
        return ret[::-1]
    return ret #default == ascending


# API: Get Method 3,
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_by_todo_id_handler(todo_id: int):
    todo = todo_data.get(todo_id, {})
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found") #no todo id
    #return todo_data.get(todo_id, {}) # else: return blank dict

# API: Post Method
class CreateToDoRequest(BaseModel):
    """
    Create Request Body (Format)
    """
    id: int
    contents: str
    is_done: bool

@app.post("/todos", status_code=201) # create
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict() # BaseModel Method
    return todo_data[request.id]

# API: Patch Method
@app.patch("/todos/{todo_id}", status_code=200) # OK
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True) #request body 중 하나만 전달
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# API: Delete Method
@app.delete("/todos/{todo_id}", status_code=204) # No Content
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    # no return.

# try : uvicorn main:app
# * uvicorn main:app --reload (auto reload)