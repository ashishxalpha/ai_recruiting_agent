from typing import Optional
from src.application.llm.interfaces import LLMProvider, LLMRequest, LLMResponse

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        # Stub implementation

    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError("AnthropicProvider not fully implemented yet")
        
    async def stream(self, request: LLMRequest):
        raise NotImplementedError("Streaming not yet implemented")
