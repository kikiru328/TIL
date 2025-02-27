from fastapi import FastAPI

from api import todo, user

app = FastAPI()
app.include_router(todo.router)
app.include_router(user.router)

# API: Get Method 1
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
# * uvicorn main:app --reload (auto reload)