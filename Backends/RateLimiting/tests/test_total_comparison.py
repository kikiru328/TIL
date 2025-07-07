import sys
sys.path.append("../")
import redis
import time
from rate_limiters.fixed_window import FixedWindowRateLimiter
from rate_limiters.sliding_window import SlidingWindowRateLimiter
from rate_limiters.token_bucket import TokenBucketRateLimiter

# Redis 연결
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 세 알고리즘 인스턴스 생성 (동일한 조건)
fixed = FixedWindowRateLimiter(redis_client, limit=5, window_seconds=10)
sliding = SlidingWindowRateLimiter(redis_client, limit=5, window_seconds=10)
token = TokenBucketRateLimiter(redis_client, capacity=5, refill_rate=0.5)  # 2초당 1개

print("=== 세 알고리즘 비교 테스트 ===")
print("조건: 10초에 5개 / Token Bucket은 2초당 1개 충전")
print()

algorithms = [
    ("Fixed Window", fixed, "fixed_ip"),
    ("Sliding Window", sliding, "sliding_ip"), 
    ("Token Bucket", token, "token_ip")
]

# 1단계: 연속 요청 테스트
print("🔥 1단계: 6번 연속 요청")
for name, limiter, ip in algorithms:
    print(f"\n{name}:")
    for i in range(6):
        result = limiter.is_allowed(ip)
        print(f"  요청 {i+1}: {result['allowed']}")

print("\n" + "="*50)

# 2단계: 시간 지난 후 테스트
print("\n⏰ 2단계: 3초 기다린 후 요청")
time.sleep(3)

for name, limiter, ip in algorithms:
    result = limiter.is_allowed(ip)
    print(f"{name}: allowed={result['allowed']}, remaining={result.get('remaining', '?')}")

print("\n" + "="*50)

# 3단계: 버스트 트래픽 테스트
print("\n💥 3단계: 버스트 트래픽 (한번에 5개)")
print("Token Bucket만 테스트 (토큰 5개 한번에 소비)")

# 새로운 Token Bucket (풀 충전 상태)
fresh_token = TokenBucketRateLimiter(redis_client, capacity=5, refill_rate=1.0)
result = fresh_token.is_allowed("burst_test", tokens_needed=5)
print(f"5개 토큰 한번에: allowed={result['allowed']}, remaining={result['remaining']}")

# 바로 추가 요청
result = fresh_token.is_allowed("burst_test")
print(f"추가 1개 요청: allowed={result['allowed']}, remaining={result['remaining']}")
