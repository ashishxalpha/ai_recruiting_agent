import logging
import asyncio
from typing import Set
from src.domain.events import DomainEvent

logger = logging.getLogger(__name__)

class EventBus:
    """Simple in-memory event bus supporting pub/sub for SSE."""
    
    _subscribers: Set[asyncio.Queue] = set()

    @classmethod
    def subscribe(cls) -> asyncio.Queue:
        q = asyncio.Queue()
        cls._subscribers.add(q)
        return q

    @classmethod
    def unsubscribe(cls, q: asyncio.Queue):
        cls._subscribers.discard(q)

    @classmethod
    def publish(cls, event: DomainEvent):
        logger.info(f"Domain Event Published: {event.__class__.__name__}", extra={"event_data": event.model_dump(mode="json")})
        
        # Broadcast to all active subscribers
        for q in cls._subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass
