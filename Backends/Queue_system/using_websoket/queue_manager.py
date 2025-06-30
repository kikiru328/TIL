from redis import asyncio as aioredis
from fastapi import WebSocket
import os, uuid
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

redis = aioredis.from_url(REDIS_URL, decode_responses=True)
QUEUE_KEY = "queue:waiting"
STATUS_PREFIX = "token:"
MAX_ACTIVE_USERS = 3
ACTIVE_TTL = 600

# WebSocket 연결 저장소
ws_map: dict[str, WebSocket] = {}

async def register_ws(token: str, websocket: WebSocket):
    ws_map[token] = websocket

async def unregister_ws(token: str):
    ws_map.pop(token, None)

async def notify_active(token: str):
    ws = ws_map.get(token)
    if ws:
        await ws.send_json({"status": "active", "message": "✅ 입장 가능!"})

async def request_token():
    token = str(uuid.uuid4())
    await redis.rpush(QUEUE_KEY, token)
    await redis.set(f"{STATUS_PREFIX}{token}", "waiting")
    return token

async def check_status(token: str):
    return await redis.get(f"{STATUS_PREFIX}{token}")

async def promote_users(notify_func=None):
    keys = await redis.keys(f"{STATUS_PREFIX}*")
    active_count = sum([1 for k in keys if await redis.get(k) == "active"])
    if active_count >= MAX_ACTIVE_USERS:
        return
    next_token = await redis.lpop(QUEUE_KEY)
    if next_token:
        await redis.set(f"{STATUS_PREFIX}{next_token}", "active", ex=ACTIVE_TTL)
        if notify_func:
            await notify_func(next_token)
