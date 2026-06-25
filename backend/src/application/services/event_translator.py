from typing import Any, Dict
from src.domain.events import DomainEvent

class EventTranslator:
    """Translates internal DomainEvents into frontend-safe payloads."""
    
    @staticmethod
    def translate(event: DomainEvent) -> Dict[str, Any]:
        """Convert a domain event into a generic UI event."""
        payload = event.model_dump(mode="json")
        
        # We can obfuscate or format fields here if needed.
        # For Sprint 7, we just add the event_type explicitly for the UI to branch on.
        return {
            "type": event.__class__.__name__,
            "data": payload
        }
