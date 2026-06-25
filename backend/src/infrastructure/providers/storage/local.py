import os
import uuid
import aiofiles

from src.domain.interfaces.providers import StorageProvider

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_path: str = "/storage"):
        self.base_path = base_path
        self.categories = [
            "candidate-documents",
            "processed",
            "temporary",
            "failed"
        ]
        
        # Ensure directory structure exists
        for category in self.categories:
            os.makedirs(os.path.join(self.base_path, category), exist_ok=True)

    async def upload(self, file_bytes: bytes, original_filename: str, category: str = "candidate-documents") -> str:
        if category not in self.categories:
            raise ValueError(f"Invalid storage category: {category}")

        ext = os.path.splitext(original_filename)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        storage_key = os.path.join(category, unique_name)
        
        full_path = os.path.join(self.base_path, storage_key)
        
        async with aiofiles.open(full_path, 'wb') as f:
            await f.write(file_bytes)
            
        return storage_key

    async def download(self, storage_key: str) -> bytes:
        full_path = os.path.join(self.base_path, storage_key)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found at {storage_key}")
            
        async with aiofiles.open(full_path, 'rb') as f:
            return await f.read()

    async def delete(self, storage_key: str) -> bool:
        full_path = os.path.join(self.base_path, storage_key)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    async def exists(self, storage_key: str) -> bool:
        full_path = os.path.join(self.base_path, storage_key)
        return os.path.exists(full_path)
