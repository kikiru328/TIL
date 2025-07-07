import time
from typing import Any, Dict
from rate_limiters import RateLimiterInterface


class NoLimitRateLimiter(RateLimiterInterface):
    """no limit, accept all requests"""
    def is_allowed(self, identifier: str) -> Dict[str, Any]:
        return {
            "allowed" : True,
            "remaining": 999999, # no limit
            "reset_time": int(time.time()) + 60, #60초
            "retry_after": 0,
            "algorithm": "no_limit",
            
        }        
        
    def get_algorithm_name(self) -> str:
        return "No Limit"
