from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi_utils.tasks import repeat_every
from queue_manager import (
    request_token, check_status, promote_users,
    register_ws, unregister_ws, notify_active
)

app = FastAPI()  # ✅ FastAPI 인스턴스 선언

@app.post("/queue/request-token")
async def create_token():
    token = await request_token()
    return {"token": token}

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()
    await register_ws(token, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await unregister_ws(token)

@app.on_event("startup")
@repeat_every(seconds=2)
async def run_promotion():
    await promote_users(notify_func=notify_active)

from fastapi.routing import APIRoute, APIWebSocketRoute

print("🚦 등록된 라우트:")
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"[HTTP]      {route.path} - {route.methods}")
    elif isinstance(route, APIWebSocketRoute):
        print(f"[WebSocket] {route.path}")
    else:
        print(f"[기타]      {route.path}")