import redis
import time
import sys
sys.path.append("../")
from rate_limiters.fixed_window import FixedWindowRateLimiter

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
limiter = FixedWindowRateLimiter(redis_client, limit=5, window_seconds=60)

print("=== Fixed Window Burst Traffic 테스트 ===")
print("경계 근처에서 요청 몰림 시뮬레이션")
print()

ip = "192.168.1.100"

# 현재 윈도우에서 5개 요청
print("1단계: 현재 윈도우에서 5개 요청")
for i in range(5):
    result = limiter.is_allowed(ip)
    print(f"요청 {i+1}: allowed={result['allowed']}")

# 1분 기다린 후 (새 윈도우)
print("\n2단계: 1분 후 새 윈도우에서 5개 요청")
print("실제로는 기다리지 말고 윈도우 경계 문제 확인용")

# 빠르게 연속 요청 (burst)
for i in range(5):
    result = limiter.is_allowed(ip)
    print(f"새윈도우 요청 {i+1}: allowed={result['allowed']}")
