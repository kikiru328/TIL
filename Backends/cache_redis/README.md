# FastAPI + Redis 캐시 기반 CRUD 예제

**FastAPI**와 **Redis**를 사용해 기본적인 **CRUD 기능**을 구현하고,  
조회(Read) 시 Redis를 활용하여 **캐시 처리**를 하는 구조입니다.

---

## 기술 스택

- **FastAPI**: 웹 API 프레임워크
- **Redis**: 인메모리 캐시 저장소
- **redis[asyncio]**: Redis 비동기 클라이언트
- **uvicorn**: FastAPI 실행 서버
- **Docker**: Redis 실행 환경

---

## 기능 요약

| 기능 | 동작 방식 |
|------|-----------|
| Create | DB에 저장 + Redis에 캐시 |
| Read   | Redis에서 먼저 조회 → 없으면 DB → Redis에 캐시 |
| Update | DB 수정 + Redis 캐시 갱신 |
| Delete | DB 삭제 + Redis 캐시 삭제 |

---

## 설치 및 실행

### 1. Redis Docker 실행

```bash
docker run --name redis -p 6379:6379 -d redis
```

### 2. 패키지 설치

```bash
pip install fastapi uvicorn[standard] redis[asyncio]
```

### 3. FastAPI 실행

```bash
uvicorn test_redis:app --reload
```

- 실행 후 Swagger 문서: http://localhost:8000/docs

## 캐시 동작 설명
	•	조회 시 먼저 Redis에서 키: user:{user_id} 를 조회합니다.
	•	Redis에 없으면 fake_db(가짜 DB)에서 조회하고 Redis에 캐시합니다.
	•	TTL은 60초로 설정되어 있어, 이후 자동 만료됩니다.

```python
await redis_client.set(key, user.model_dump_json(), ex=60)
```

### TIL 확인 방법

```bash
docker exec -it redis redis-cli
TTL user:1
```
