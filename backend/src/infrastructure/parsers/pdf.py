import fitz  # PyMuPDF
from .base import DocumentParser, DocumentContent
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class PDFParser(DocumentParser):
    def parse(self, file_bytes: bytes) -> DocumentContent:
        with tracer.start_as_current_span("PDFParser.parse"):
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
                
            text = "\n".join(text_parts).strip()
            
            metadata = {
                "format": "pdf",
                "author": doc.metadata.get("author"),
                "title": doc.metadata.get("title")
            }
            
            return DocumentContent(
                text=text,
                page_count=len(doc),
                metadata=metadata
            )
