class ExtractionFailedException(Exception):
    """Raised when text or AI extraction fails generally."""
    pass

class ValidationFailedException(Exception):
    """Raised when the extracted profile fails business rule validation."""
    pass

class ProviderTimeoutException(Exception):
    """Raised when the AI provider times out. This is a recoverable error."""
    pass

class ProviderRateLimitException(Exception):
    """Raised when the AI provider rate limits. This is a recoverable error."""
    pass

class ProviderUnavailableException(Exception):
    """Raised when the AI provider is unavailable. This is a recoverable error."""
    pass
