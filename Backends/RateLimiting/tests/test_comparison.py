import redis
import time
import sys
sys.path.append("../")
from rate_limiters.fixed_window import FixedWindowRateLimiter
from rate_limiters.sliding_window import SlidingWindowRateLimiter

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

fixed = FixedWindowRateLimiter(redis_client, limit=5, window_seconds=10)
sliding = SlidingWindowRateLimiter(redis_client, limit=5, window_seconds=10)

print("=== Fixed vs Sliding 경계 문제 비교 ===")
print()

# 경계 근처 테스트를 위해 윈도우 끝 2초 전 시뮬레이션
print("Fixed Window 테스트:")
for i in range(7):
    result = fixed.is_allowed("192.168.1.100")
    print(f"요청 {i+1}: {result['allowed']}")

print("\nSliding Window 테스트:")  
for i in range(7):
    result = sliding.is_allowed("192.168.1.200")
    print(f"요청 {i+1}: {result['allowed']}")
