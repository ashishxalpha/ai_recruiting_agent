from typing import List, Dict, Any, Optional, Protocol
from pydantic import BaseModel

class LLMUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float = 0.0

class LLMToolCall(BaseModel):
    id: str
    function_name: str
    function_arguments: str # JSON string

class LLMMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[LLMToolCall]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class LLMResponse(BaseModel):
    content: Optional[str]
    tool_calls: Optional[List[LLMToolCall]]
    usage: LLMUsage
    model: str
    finish_reason: Optional[str]

class LLMRequest(BaseModel):
    messages: List[LLMMessage]
    model: Optional[str] = None
    temperature: float = 0.0
    top_p: float = 1.0
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Any] = None
    seed: Optional[int] = None
    max_tokens: Optional[int] = None

class LLMProvider(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        ...
        
    async def stream(self, request: LLMRequest):
        ...
