# framework
from fastapi import FastAPI

app = FastAPI()

# API: Get method
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}