import asyncio
import logging
from typing import Callable, Any, Awaitable, TypeVar
from src.domain.exceptions import ProviderRateLimitException, ProviderTimeoutException

T = TypeVar('T')

class RetryPolicy:
    async def execute(self, func: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
        raise NotImplementedError

class ExponentialBackoffRetryPolicy(RetryPolicy):
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute(self, func: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
        retries = 0
        while True:
            try:
                return await func(*args, **kwargs)
            except (ProviderRateLimitException, ProviderTimeoutException) as e:
                if retries >= self.max_retries:
                    raise
                
                delay = min(self.base_delay * (2 ** retries), self.max_delay)
                logging.warning(f"Retrying AI provider call in {delay} seconds due to {type(e).__name__}")
                await asyncio.sleep(delay)
                retries += 1
