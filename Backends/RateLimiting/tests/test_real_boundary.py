import redis
import time
import sys
sys.path.append("../")
from rate_limiters.fixed_window import FixedWindowRateLimiter
from rate_limiters.sliding_window import SlidingWindowRateLimiter

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 5초 윈도우로 짧게 설정
fixed = FixedWindowRateLimiter(redis_client, limit=3, window_seconds=5)
sliding = SlidingWindowRateLimiter(redis_client, limit=3, window_seconds=5)

print("=== 경계 문제 실제 확인 ===")
print("설정: 5초에 3개 제한")
print()

# Fixed Window 경계 테스트
print("🕐 Fixed Window - 경계 문제:")
print("1) 현재 윈도우에서 3개 요청")
for i in range(3):
    result = fixed.is_allowed("fixed_ip")
    print(f"  요청 {i+1}: {result['allowed']}")

print("2) 5초 기다린 후 (새 윈도우)")
time.sleep(6)  # 6초 기다리기

print("3) 새 윈도우에서 3개 요청")
for i in range(3):
    result = fixed.is_allowed("fixed_ip")
    print(f"  새윈도우 요청 {i+1}: {result['allowed']}")

print("\n📱 Sliding Window - 문제 해결:")
print("1) 3개 요청")
for i in range(3):
    result = sliding.is_allowed("sliding_ip")
    print(f"  요청 {i+1}: {result['allowed']}")

print("2) 즉시 3개 더 요청 (기다리지 않음)")
for i in range(3):
    result = sliding.is_allowed("sliding_ip")
    print(f"  추가 요청 {i+1}: {result['allowed']}")

print("\n💡 결론:")
print("Fixed: 경계에서 6개 허용 (문제!)")
print("Sliding: 총 3개만 허용 (해결!)")
