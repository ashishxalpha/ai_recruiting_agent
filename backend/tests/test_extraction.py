import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4

from src.application.schemas.extraction import CandidateProfile, Skill
from src.infrastructure.providers.ai.openai import OpenAIExtractionProvider
from src.infrastructure.providers.ai.retry import ExponentialBackoffRetryPolicy
from src.domain.exceptions import ProviderRateLimitException
import openai

@pytest.fixture
def mock_openai():
    with patch("src.infrastructure.providers.ai.openai.AsyncOpenAI") as mock:
        yield mock

@pytest.mark.asyncio
async def test_openai_extraction_success(mock_openai):
    # Setup mock response
    mock_client = AsyncMock()
    mock_openai.return_value = mock_client
    
    mock_completion = MagicMock()
    mock_message = MagicMock()
    mock_message.refusal = None
    
    # Construct a sample Pydantic parsed output
    parsed_profile = CandidateProfile(
        first_name="John",
        last_name="Doe",
        skills=[Skill(name="Python", proficiency="Expert")]
    )
    mock_message.parsed = parsed_profile
    mock_message.content = '{"first_name": "John"}'
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    mock_usage = MagicMock()
    mock_usage.prompt_tokens = 100
    mock_usage.completion_tokens = 50
    mock_usage.total_tokens = 150
    mock_completion.usage = mock_usage
    
    mock_client.beta.chat.completions.parse.return_value = mock_completion
    
    provider = OpenAIExtractionProvider(api_key="test")
    profile, metrics = await provider.extract_profile("raw resume text", "Prompt: {{text}}")
    
    assert profile.first_name == "John"
    assert len(profile.skills) == 1
    assert profile.skills[0].name == "Python"
    
    assert metrics["input_tokens"] == 100
    assert metrics["provider"] == "openai"

@pytest.mark.asyncio
async def test_openai_extraction_retry_policy():
    func = AsyncMock()
    # Fail twice, succeed third time
    func.side_effect = [
        ProviderRateLimitException("Rate limit"),
        ProviderRateLimitException("Rate limit"),
        "Success"
    ]
    
    policy = ExponentialBackoffRetryPolicy(max_retries=3, base_delay=0.01)
    
    result = await policy.execute(func)
    
    assert result == "Success"
    assert func.call_count == 3

@pytest.mark.asyncio
async def test_openai_extraction_retry_policy_failure():
    func = AsyncMock()
    # Always fail
    func.side_effect = ProviderRateLimitException("Rate limit")
    
    policy = ExponentialBackoffRetryPolicy(max_retries=2, base_delay=0.01)
    
    with pytest.raises(ProviderRateLimitException):
        await policy.execute(func)
        
    assert func.call_count == 3  # Initial + 2 retries
