import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.infrastructure.events.event_bus import EventBus
from src.application.services.event_translator import EventTranslator

router = APIRouter()

@router.get("")
async def stream_events():
    """Server-Sent Events endpoint to stream real-time workflow events."""
    
    async def event_generator():
        # Subscribe to internal EventBus
        q = EventBus.subscribe()
        try:
            while True:
                # Wait for the next event
                event = await q.get()
                
                # Translate domain event to frontend-safe payload
                frontend_payload = EventTranslator.translate(event)
                
                # Yield SSE formatted string
                data_str = json.dumps(frontend_payload)
                yield f"data: {data_str}\n\n"
                
                # Let event loop breathe
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            # Client disconnected
            EventBus.unsubscribe(q)
            raise
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
