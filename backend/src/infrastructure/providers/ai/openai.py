import time
from typing import Dict, Any, Tuple
from openai import AsyncOpenAI
import openai
from src.application.schemas.extraction import CandidateProfile
from src.domain.exceptions import (
    ProviderRateLimitException, 
    ProviderTimeoutException, 
    ProviderUnavailableException,
    ExtractionFailedException
)
from src.observability.tracing import get_tracer
from .retry import RetryPolicy, ExponentialBackoffRetryPolicy

tracer = get_tracer(__name__)

class AIExtractionProvider:
    async def extract_profile(self, raw_text: str, prompt_template: str) -> Tuple[CandidateProfile, Dict[str, Any]]:
        raise NotImplementedError

class OpenAIExtractionProvider(AIExtractionProvider):
    def __init__(self, api_key: str, model_name: str = "gpt-4o-2024-08-06", retry_policy: RetryPolicy = None):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model_name = model_name
        self.retry_policy = retry_policy or ExponentialBackoffRetryPolicy()

    async def extract_profile(self, raw_text: str, prompt_template: str) -> Tuple[CandidateProfile, Dict[str, Any]]:
        # Compile prompt
        prompt = prompt_template.replace("{{text}}", raw_text)
        
        async def _call_api():
            start_time = time.time()
            try:
                completion = await self.client.beta.chat.completions.parse(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": prompt}
                    ],
                    response_format=CandidateProfile,
                )
                processing_time_ms = int((time.time() - start_time) * 1000)
                
                if completion.choices[0].message.refusal:
                    raise ExtractionFailedException(f"Model refused: {completion.choices[0].message.refusal}")
                    
                profile = completion.choices[0].message.parsed
                raw_json = completion.choices[0].message.content
                
                usage = completion.usage
                metrics = {
                    "input_tokens": usage.prompt_tokens if usage else 0,
                    "output_tokens": usage.completion_tokens if usage else 0,
                    "total_tokens": usage.total_tokens if usage else 0,
                    "processing_time_ms": processing_time_ms,
                    "model_name": self.model_name,
                    "provider": "openai",
                    "raw_response": profile.model_dump(), # Storing the parsed output since we used Structured Outputs
                }
                
                return profile, metrics
                
            except openai.RateLimitError as e:
                raise ProviderRateLimitException(str(e))
            except openai.APITimeoutError as e:
                raise ProviderTimeoutException(str(e))
            except openai.APIConnectionError as e:
                raise ProviderUnavailableException(str(e))
            except openai.OpenAIError as e:
                raise ExtractionFailedException(f"OpenAI API error: {str(e)}")

        with tracer.start_as_current_span("OpenAIExtractionProvider.extract_profile"):
            return await self.retry_policy.execute(_call_api)
