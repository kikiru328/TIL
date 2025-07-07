import redis
import time
import sys
sys.path.append("../")
from rate_limiters.fixed_window import FixedWindowRateLimiter


# Redis 연결 (Redis 서버가 실행 중이어야 함)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Fixed Window 인스턴스 생성
limiter = FixedWindowRateLimiter(redis_client, limit=5, window_seconds=60)

print("=== Fixed Window 테스트 ===")
print(f"알고리즘: {limiter.get_algorithm_name()}")
print(f"제한: 1분에 5개")
print()

# 연속 요청 테스트
ip = "192.168.1.100"
for i in range(7):
    result = limiter.is_allowed(ip)
    print(f"요청 {i+1}: allowed={result['allowed']}, remaining={result['remaining']}, retry_after={result['retry_after']}")
    time.sleep(1)

print("\n=== 다른 IP 테스트 ===")
# 다른 IP로 테스트
other_ip = "192.168.1.200"
result = limiter.is_allowed(other_ip)
print(f"다른IP 요청: allowed={result['allowed']}, remaining={result['remaining']}")
