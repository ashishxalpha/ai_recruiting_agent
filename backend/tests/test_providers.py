import pytest
import os
import aiofiles
from unittest.mock import patch, MagicMock

from src.infrastructure.providers.storage.local import LocalStorageProvider
from src.infrastructure.providers.jobs.fastapi_dispatcher import FastAPIJobDispatcher

@pytest.mark.asyncio
async def test_local_storage_provider(tmp_path):
    base = str(tmp_path)
    provider = LocalStorageProvider(base_path=base)
    
    # Test upload
    key = await provider.upload(b"test data", "doc.pdf", category="candidate-documents")
    assert key.startswith("candidate-documents/")
    assert key.endswith(".pdf")
    
    # Test exists
    assert await provider.exists(key) is True
    
    # Test download
    data = await provider.download(key)
    assert data == b"test data"
    
    # Test delete
    assert await provider.delete(key) is True
    assert await provider.exists(key) is False

@pytest.mark.asyncio
async def test_fastapi_job_dispatcher():
    background_tasks = MagicMock()
    dispatcher = FastAPIJobDispatcher(background_tasks)
    
    await dispatcher.dispatch("test_job", {"id": "123"})
    background_tasks.add_task.assert_called_once_with(dispatcher._dummy_task, "test_job", {"id": "123"})
