import time
import redis
from typing import Dict, Any
from . import RateLimiterInterface

class SlidingWindowRateLimiter(RateLimiterInterface):
    """Sliding Window Rate Limiting - 모든 요청 시간을 기록하여 정확한 제어"""
    
    def __init__(self, redis_client, limit: int = 5, window_seconds: int = 60):
        self.redis = redis_client  # Redis 클라이언트 저장
        self.limit = limit  # 제한 개수 (기본: 5개)
        self.window_seconds = window_seconds  # 윈도우 시간 (기본: 60초)
    
    def is_allowed(self, identifier: str) -> Dict[str, Any]:
        current_time = time.time()  # 현재 시간 (소수점 포함)
        window_start = current_time - self.window_seconds  # 윈도우 시작점 계산
        
        redis_key = f"sliding_window:{identifier}"  # Redis 키 생성
        
        try:
            # Lua 스크립트로 원자적 연산 수행 (동시성 문제 해결)
            lua_script = """
            local key = KEYS[1]                    -- Redis 키
            local window_start = tonumber(ARGV[1]) -- 윈도우 시작 시간
            local current_time = tonumber(ARGV[2]) -- 현재 시간
            local limit = tonumber(ARGV[3])        -- 제한 개수
            
            -- 1. 윈도우 밖의 오래된 요청들 제거
            redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
            
            -- 2. 현재 윈도우 내 요청 수 확인
            local current_count = redis.call('ZCARD', key)
            
            -- 3. 제한 초과 체크
            if current_count >= limit then
                return 0  -- 거절
            end
            
            -- 4. 새 요청 추가 (현재 시간을 score로 사용)
            redis.call('ZADD', key, current_time, current_time)
            
            -- 5. 키 만료 시간 설정 (메모리 절약)
            redis.call('EXPIRE', key, math.ceil(tonumber(ARGV[4])))
            
            return 1  -- 허용
            """
            
            # Lua 스크립트 실행
            result = self.redis.eval(
                lua_script, 
                1,  # 키 개수
                redis_key,  # KEYS[1]
                window_start,  # ARGV[1] 
                current_time,  # ARGV[2]
                self.limit,  # ARGV[3]
                self.window_seconds  # ARGV[4]
            )
            
            if result == 0:  # 거절된 경우
                # 현재 윈도우 내 요청 수 다시 확인 (remaining 계산용)
                current_count = self.redis.zcard(redis_key)
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_time": int(current_time + self.window_seconds),  # 대략적 리셋 시간
                    "retry_after": 1,  # 1초 후 다시 시도 (정확한 계산 복잡)
                    "algorithm": "sliding_window"
                }
            else:  # 허용된 경우
                # 새로 추가된 후의 요청 수 확인
                current_count = self.redis.zcard(redis_key)
                return {
                    "allowed": True,
                    "remaining": self.limit - current_count,
                    "reset_time": int(current_time + self.window_seconds),
                    "retry_after": 0,
                    "algorithm": "sliding_window"
                }
                
        except redis.RedisError as e:  # Redis 오류 처리
            print(f"Redis error: {e}")
            return {
                "allowed": True,  # 오류 시 안전하게 허용
                "remaining": self.limit - 1,
                "reset_time": int(current_time + self.window_seconds),
                "retry_after": 0,
                "algorithm": "sliding_window"
            }
    
    def get_algorithm_name(self) -> str:
        return "Sliding Window"  # 알고리즘 이름 반환
