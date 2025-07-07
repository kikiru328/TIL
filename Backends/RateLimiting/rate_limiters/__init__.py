from abc import ABC, abstractmethod
from typing import Dict, Any

class RateLimiterInterface(ABC):
    """ common interface"""
    @abstractmethod
    def is_allowed(self, identifier: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_algorithm_name(self) -> str:
        pass
