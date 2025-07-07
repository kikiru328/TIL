import redis
import time
import sys
sys.path.append("../")
from rate_limiters.sliding_window import SlidingWindowRateLimiter

# Redis 연결
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Sliding Window 인스턴스 생성 (10초에 5개 제한)
limiter = SlidingWindowRateLimiter(redis_client, limit=5, window_seconds=10)

print("=== Sliding Window 테스트 ===")
print(f"알고리즘: {limiter.get_algorithm_name()}")
print(f"제한: 10초에 5개")
print()

ip = "192.168.1.100"

# 1단계: 7번 연속 요청
print("1단계: 7번 연속 요청")
for i in range(7):
    result = limiter.is_allowed(ip)
    print(f"요청 {i+1}: allowed={result['allowed']}, remaining={result['remaining']}")
    time.sleep(1)  # 1초 간격

print()

# 2단계: 5초 기다린 후 요청
print("2단계: 5초 기다린 후 요청")
time.sleep(5)
result = limiter.is_allowed(ip)
print(f"5초 후 요청: allowed={result['allowed']}, remaining={result['remaining']}")

print()

# 3단계: 다른 IP 테스트
print("3단계: 다른 IP 테스트")
other_ip = "192.168.1.200"
result = limiter.is_allowed(other_ip)
print(f"다른IP 요청: allowed={result['allowed']}, remaining={result['remaining']}")
