from docx import Document
from io import BytesIO
from .base import DocumentParser, DocumentContent
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class DOCXParser(DocumentParser):
    def parse(self, file_bytes: bytes) -> DocumentContent:
        with tracer.start_as_current_span("DOCXParser.parse"):
            doc = Document(BytesIO(file_bytes))
            
            text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
            text = "\n".join(text_parts).strip()
            
            # DOCX doesn't have a reliable 'page count' natively since it's flow-based.
            # We estimate 1 page per 3000 characters.
            page_count = max(1, len(text) // 3000)
            
            metadata = {
                "format": "docx",
                "core_properties": {
                    "author": doc.core_properties.author,
                    "title": doc.core_properties.title,
                }
            }
            
            return DocumentContent(
                text=text,
                page_count=page_count,
                metadata=metadata
            )
