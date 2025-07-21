from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis

app = FastAPI()

# Redis 연결
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 가짜 DB
fake_db = {}

# 사용자 모델
class User(BaseModel):
    id: str
    name: str

# Redis 키 생성 함수
def get_redis_key(user_id: str) -> str:
    return f"user:{user_id}"

# Create
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.id in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # 1. DB 저장
    fake_db[user.id] = user.dict()

    # 2. Redis 저장
    key = get_redis_key(user.id)
    await redis_client.set(key, user.model_dump_json(), ex=60)

    return user

# Read
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    key = get_redis_key(user_id)

    # 1. Redis 조회
    cached = await redis_client.get(key)
    if cached:
        print("🔥 from cache")
        return User.model_validate_json(cached)

    # 2. DB 조회
    user = fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Redis 저장
    await redis_client.set(key, User(**user).model_dump_json(), ex=60)
    print("📦 from db + cached")

    return user

# Update
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. DB 갱신
    fake_db[user_id] = user.dict()

    # 2. Redis 갱신
    key = get_redis_key(user_id)
    await redis_client.set(key, user.model_dump_json(), ex=60)

    return user

# Delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. DB 삭제
    del fake_db[user_id]

    # 2. Redis 삭제
    key = get_redis_key(user_id)
    await redis_client.delete(key)

    return {"detail": "User deleted"}
