# test_window_boundary.py
import redis
import time
import sys
sys.path.append("../")
from rate_limiters.fixed_window import FixedWindowRateLimiter

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
limiter = FixedWindowRateLimiter(redis_client, limit=5, window_seconds=10)  # 10초로 짧게!

print("=== 윈도우 경계 문제 시뮬레이션 ===")
print("윈도우: 10초, 제한: 5개")
print()

ip = "192.168.1.100"

# 현재 시간 확인
current_time = int(time.time())
window_start = (current_time // 10) * 10
window_end = window_start + 10

print(f"현재 윈도우: {window_start} ~ {window_end}")
print(f"현재 시간: {current_time}")
print()

# 윈도우 끝 2초 전에 5개 요청
print("1. 윈도우 끝 직전에 5개 요청:")
for i in range(5):
    result = limiter.is_allowed(ip)
    print(f"  요청 {i+1}: allowed={result['allowed']}")

print(f"\n2. 새 윈도우 시작까지 기다리는 중...")
# 새 윈도우까지 기다리기
while int(time.time()) < window_end:
    time.sleep(0.1)

print("3. 새 윈도우에서 즉시 5개 요청:")
for i in range(5):
    result = limiter.is_allowed(ip)
    print(f"  새윈도우 요청 {i+1}: allowed={result['allowed']}")

print("\n💥 결과: 20초 안에 10개 요청 처리됨! (원래는 10초에 5개 제한)")
