import os
import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from src.infrastructure.config import get_openai_api_key
from src.application.llm.interfaces import (
    LLMProvider, LLMRequest, LLMResponse, LLMMessage, LLMToolCall, LLMUsage
)

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key or get_openai_api_key())
        self.default_model = "gpt-4o"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        # Convert internal messages to OpenAI format
        openai_messages = []
        for msg in request.messages:
            om: Dict[str, Any] = {"role": msg.role, "content": msg.content or ""}
            if msg.name:
                om["name"] = msg.name
            if msg.tool_call_id:
                om["tool_call_id"] = msg.tool_call_id
            if msg.tool_calls:
                om["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function_name,
                            "arguments": tc.function_arguments
                        }
                    } for tc in msg.tool_calls
                ]
            openai_messages.append(om)

        kwargs = {
            "model": request.model or self.default_model,
            "messages": openai_messages,
            "temperature": request.temperature,
            "top_p": request.top_p,
        }
        
        if request.tools:
            kwargs["tools"] = request.tools
        if request.tool_choice:
            kwargs["tool_choice"] = request.tool_choice
        if request.seed is not None:
            kwargs["seed"] = request.seed
        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens

        response = await self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        msg = choice.message
        
        tool_calls = None
        if msg.tool_calls:
            tool_calls = [
                LLMToolCall(
                    id=tc.id,
                    function_name=tc.function.name,
                    function_arguments=tc.function.arguments
                ) for tc in msg.tool_calls
            ]
            
        usage = LLMUsage(
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
            total_tokens=response.usage.total_tokens if response.usage else 0,
            cost=0.0 # Calculate based on model in a real implementation
        )

        return LLMResponse(
            content=msg.content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            finish_reason=choice.finish_reason
        )
        
    async def stream(self, request: LLMRequest):
        raise NotImplementedError("Streaming not yet implemented")
