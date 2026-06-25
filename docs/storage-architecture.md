# Storage Architecture

The Copilot leverages a Provider-based storage abstraction to decouple the local filesystem from cloud providers (AWS S3, Google Cloud Storage, etc.).

## Directory Structure
For Sprint 3 (Local Development), storage maps to the following mounted volumes:

```text
/storage
├── /candidate-documents  # Raw uploaded PDF/DOCX resumes
├── /processed            # Extracted text/images or normalized data
├── /temporary            # In-flight processing files
└── /failed               # Files that failed parsing/extraction
```

## Storage Provider Interface

```python
class StorageProvider(Protocol):
    async def upload(self, file_bytes: bytes, original_filename: str, category: str = "candidate-documents") -> str: ...
    async def download(self, storage_key: str) -> bytes: ...
    async def delete(self, storage_key: str) -> bool: ...
    async def exists(self, storage_key: str) -> bool: ...
```
