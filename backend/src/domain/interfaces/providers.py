from typing import Protocol

class StorageProvider(Protocol):
    async def upload(self, file_bytes: bytes, original_filename: str, category: str = "candidate-documents") -> str:
        """Upload a file and return its storage key/path."""
        ...

    async def download(self, storage_key: str) -> bytes:
        """Download a file by its storage key/path."""
        ...

    async def delete(self, storage_key: str) -> bool:
        """Delete a file by its storage key/path."""
        ...

    async def exists(self, storage_key: str) -> bool:
        """Check if a file exists by its storage key/path."""
        ...

class JobDispatcher(Protocol):
    async def dispatch(self, job_name: str, payload: dict) -> None:
        """Dispatch a background job."""
        ...
