import time
import asyncio
from enum import Enum
from typing import Dict, Any

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, cooldown_seconds: int = 30):
        self.state = CircuitState.CLOSED
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        
        self.failure_count = 0
        self.last_failure_time = 0.0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            # Failed while half-open -> immediately open
            self.state = CircuitState.OPEN
        elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
        self.failure_count = 0

    def allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.cooldown_seconds:
                # Cooldown passed, transition to half-open
                self.state = CircuitState.HALF_OPEN
                return True
            return False
            
        if self.state == CircuitState.HALF_OPEN:
            # We already let one request through to test it, if another comes in concurrently, 
            # we might want to fail fast or queue. For simplicity, we allow it.
            return True
            
        return False

class CircuitBreakerManager:
    def __init__(self, default_threshold: int = 3, default_cooldown: int = 30):
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.default_threshold = default_threshold
        self.default_cooldown = default_cooldown
        
    def configure(self, provider_id: str, failure_threshold: int, cooldown_seconds: int):
        if provider_id not in self.breakers:
            self.breakers[provider_id] = CircuitBreaker(failure_threshold, cooldown_seconds)
        else:
            self.breakers[provider_id].failure_threshold = failure_threshold
            self.breakers[provider_id].cooldown_seconds = cooldown_seconds

    def get_breaker(self, provider_id: str) -> CircuitBreaker:
        if provider_id not in self.breakers:
            self.breakers[provider_id] = CircuitBreaker(self.default_threshold, self.default_cooldown)
        return self.breakers[provider_id]
