import time
from rate_limiters import RateLimiterInterface
import redis
from typing import Dict, Any

class FixedWindowRateLimiter(RateLimiterInterface):
    def __init__(self, redis_client, limit: int = 5, window_seconds: int = 60):
        self.redis = redis_client
        self.limit = limit
        self.window_seconds = window_seconds
        
    def is_allowed(self, identifier: str) -> Dict[str, Any]:
        current_time = int(time.time())
        window_start = (current_time // self.window_seconds) * self.window_seconds
        redis_key = f"fixed_window:{identifier}:{window_start}"
        try: 
            current_count = self.redis.get(redis_key) # 현재 요청 수
            current_count = int(current_count) if current_count else 0
            if current_count >= self.limit:
                return {
                    "allowed": False, #요청 거절
                    "remaining": 0, #남은 요청수 없음
                    "reset_time": window_start + self.window_seconds, # 윈도우 리셋
                    "retry_after": (window_start + self.window_seconds) - current_time, #재시도 시간 명시
                    "algorithm": "fixed_window"
                }
                
            pipe = self.redis.pipeline() # 요청 수 증가
            pipe.incr(redis_key) # redis += 1
            pipe.expire(redis_key, self.window_seconds) # 만료시간 설정
            pipe.execute()
            
            return {
                "allowed": True, #요청 허용
                "remaining": self.limit - (current_count + 1), # 남은 요청 개수
                "reset_time": window_start + self.window_seconds,
                "retry_after": 0,
                "algorithm": "fixed_window"
            }
        except redis.RedisError as e:
            print(f"Redis error: {e}")        
            return {
                "allowed": True,
                "remaining": self.limit - 1,
                "reset_time": window_start + self.window_seconds,
                "retry_after": 0,
                "algorithm": "fixed_window"
            }
            
    def get_algorithm_name(self) -> str:
        return "Fixed Window"
