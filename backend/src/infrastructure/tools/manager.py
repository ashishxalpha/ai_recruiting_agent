from typing import Dict
from src.application.tools.interfaces import ProviderManager, ToolProvider

class DefaultProviderManager(ProviderManager):
    def __init__(self):
        self._providers: Dict[str, ToolProvider] = {}

    async def register_provider(self, provider: ToolProvider) -> None:
        self._providers[provider.provider_id] = provider
        await provider.connect()

    async def get_provider(self, provider_id: str) -> ToolProvider:
        return self._providers.get(provider_id)

    async def monitor_health(self) -> None:
        for provider in self._providers.values():
            await provider.health()
