import time
import redis
from typing import Dict, Any
from . import RateLimiterInterface

class TokenBucketRateLimiter(RateLimiterInterface):
    """Token Bucket Rate Limiting - 토큰을 소비하여 버스트 트래픽 허용"""
    
    def __init__(self, redis_client, capacity: int = 5, refill_rate: float = 1.0):
        self.redis = redis_client  # Redis 클라이언트
        self.capacity = capacity  # 버킷 최대 용량 (기본: 5개)
        self.refill_rate = refill_rate  # 초당 토큰 충전률 (기본: 1개/초)
    
    def is_allowed(self, identifier: str, tokens_needed: int = 1) -> Dict[str, Any]:
        current_time = time.time()  # 현재 시간 (소수점 포함)
        redis_key = f"token_bucket:{identifier}"  # Redis 키
        
        try:
            # Lua 스크립트로 원자적 연산
            lua_script = """
            local key = KEYS[1]
            local capacity = tonumber(ARGV[1])      -- 버킷 최대 용량
            local refill_rate = tonumber(ARGV[2])   -- 초당 충전률
            local tokens_needed = tonumber(ARGV[3]) -- 필요한 토큰 수
            local current_time = tonumber(ARGV[4])  -- 현재 시간
            
            -- 버킷 정보 가져오기 (토큰 수, 마지막 충전 시간)
            local bucket_data = redis.call('HMGET', key, 'tokens', 'last_refill')
            local tokens = tonumber(bucket_data[1]) or capacity  -- 토큰 수 (없으면 풀로 시작)
            local last_refill = tonumber(bucket_data[2]) or current_time  -- 마지막 충전 시간
            
            -- 토큰 충전 계산
            local elapsed = current_time - last_refill  -- 경과 시간
            local new_tokens = math.min(capacity, tokens + elapsed * refill_rate)  -- 충전된 토큰 수
            
            -- 토큰 부족 체크
            if new_tokens < tokens_needed then
                -- 토큰 부족 시 현재 상태만 업데이트 (토큰 소비 안 함)
                redis.call('HMSET', key, 'tokens', new_tokens, 'last_refill', current_time)
                redis.call('EXPIRE', key, 3600)  -- 1시간 후 만료
                return {0, new_tokens}  -- {거절, 현재토큰수}
            end
            
            -- 토큰 소비
            local remaining_tokens = new_tokens - tokens_needed
            
            -- 상태 저장
            redis.call('HMSET', key, 'tokens', remaining_tokens, 'last_refill', current_time)
            redis.call('EXPIRE', key, 3600)
            
            return {1, remaining_tokens}  -- {허용, 남은토큰수}
            """
            
            # Lua 스크립트 실행
            result = self.redis.eval(
                lua_script,
                1,  # 키 개수
                redis_key,  # KEYS[1]
                self.capacity,  # ARGV[1]
                self.refill_rate,  # ARGV[2] 
                tokens_needed,  # ARGV[3]
                current_time  # ARGV[4]
            )
            
            allowed = result[0] == 1  # 허용 여부
            remaining_tokens = result[1]  # 남은 토큰 수
            
            if allowed:
                return {
                    "allowed": True,
                    "remaining": int(remaining_tokens),
                    "reset_time": int(current_time + (self.capacity / self.refill_rate)),  # 풀 충전까지 시간
                    "retry_after": 0,
                    "algorithm": "token_bucket"
                }
            else:
                # 토큰 부족 시 언제 충전될지 계산
                tokens_shortage = tokens_needed - remaining_tokens
                wait_time = tokens_shortage / self.refill_rate
                
                return {
                    "allowed": False,
                    "remaining": int(remaining_tokens),
                    "reset_time": int(current_time + wait_time),
                    "retry_after": int(wait_time) + 1,  # 1초 여유
                    "algorithm": "token_bucket"
                }
                
        except redis.RedisError as e:  # Redis 오류 처리
            print(f"Redis error: {e}")
            return {
                "allowed": True,  # 오류 시 허용
                "remaining": self.capacity - 1,
                "reset_time": int(current_time + 60),
                "retry_after": 0,
                "algorithm": "token_bucket"
            }
    
    def get_algorithm_name(self) -> str:
        return "Token Bucket"  # 알고리즘
