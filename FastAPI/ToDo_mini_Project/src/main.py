from fastapi import FastAPI

from api import todo

app = FastAPI()
app.include_router(todo.router)

# API: Get Method 1
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
# * uvicorn main:app --reload (auto reload)