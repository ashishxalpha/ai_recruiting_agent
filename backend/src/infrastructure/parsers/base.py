from typing import Protocol, Dict, Any
from pydantic import BaseModel

class DocumentContent(BaseModel):
    text: str
    page_count: int
    metadata: Dict[str, Any]

class DocumentParser(Protocol):
    def parse(self, file_bytes: bytes) -> DocumentContent:
        """Parse raw bytes and extract document content."""
        ...
