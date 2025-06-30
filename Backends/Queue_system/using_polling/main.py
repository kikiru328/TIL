from fastapi import FastAPI, HTTPException
from queue_manager import request_token, check_status, promote_users
from fastapi_utils.tasks import repeat_every

app = FastAPI()

active_ws_connections = {}


@app.post("/queue/request-token")
async def create_token():
    token = await request_token()
    return {"token": token}

@app.get("/queue/check-status")
async def get_status(token: str):
    status = await check_status(token)
    if status is None:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"status": status}

# 주기적으로 순번 처리
@app.on_event("startup")
@repeat_every(seconds=2)
async def background_task():
    await promote_users()
