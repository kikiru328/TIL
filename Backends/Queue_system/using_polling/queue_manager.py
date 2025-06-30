from redis import asyncio as aioredis
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

QUEUE_KEY = "queue:waiting"
STATUS_PREFIX = "token:"
MAX_ACTIVE_USERS = 3
ACTIVE_TTL = 600  # 초 단위 (10분)

redis = aioredis.from_url(REDIS_URL, decode_responses=True)

# 1. 토큰 발급 → 대기열 등록
async def request_token():
    token = str(uuid.uuid4())
    await redis.rpush(QUEUE_KEY, token)  # 대기열 등록
    await redis.set(f"{STATUS_PREFIX}{token}", "waiting")
    return token

# 2. 토큰 상태 확인
async def check_status(token: str):
    return await redis.get(f"{STATUS_PREFIX}{token}")

# 3. 최대 접속자 이하라면 → 순서대로 active 전환
async def promote_users():
    all_keys = await redis.keys(f"{STATUS_PREFIX}*")
    active_count = sum([
        1 for key in all_keys if await redis.get(key) == "active"
    ])
    if active_count >= MAX_ACTIVE_USERS:
        return

    next_token = await redis.lpop(QUEUE_KEY)
    if next_token:
        await redis.set(f"{STATUS_PREFIX}{next_token}", "active", ex=ACTIVE_TTL)
