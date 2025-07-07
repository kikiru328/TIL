import sys
sys.path.append('../')
import redis
import time
from rate_limiters.token_bucket import TokenBucketRateLimiter

# Redis 연결
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Token Bucket 생성 (용량: 5개, 초당 1개 충전)
limiter = TokenBucketRateLimiter(redis_client, capacity=5, refill_rate=1.0)

print("=== Token Bucket 테스트 ===")
print(f"알고리즘: {limiter.get_algorithm_name()}")
print(f"설정: 용량 5개, 초당 1개 충전")
print()

ip = "192.168.1.100"

# 1단계: 연속 요청 테스트
print("1단계: 7번 연속 요청")
for i in range(7):
    result = limiter.is_allowed(ip)
    print(f"요청 {i+1}: allowed={result['allowed']}, remaining={result['remaining']}, retry_after={result['retry_after']}")

print()

# 2단계: 시간 지난 후 테스트
print("2단계: 3초 기다린 후 요청")
time.sleep(3)
result = limiter.is_allowed(ip)
print(f"3초 후: allowed={result['allowed']}, remaining={result['remaining']}")

print()

# 3단계: 큰 요청 테스트
print("3단계: 토큰 3개 필요한 요청")
result = limiter.is_allowed(ip, tokens_needed=3)
print(f"3개 토큰: allowed={result['allowed']}, remaining={result['remaining']}")
