from typing import Dict, List, Optional
import datetime

from src.application.tools.interfaces import ProviderManager, ToolProvider, ProviderStatus

class InMemoryProviderManager(ProviderManager):
    def __init__(self):
        self._providers: Dict[str, ToolProvider] = {}
        self._statuses: Dict[str, ProviderStatus] = {}

    async def register_provider(self, provider: ToolProvider) -> None:
        self._providers[provider.provider_id] = provider
        # Automatically connect on register
        try:
            await provider.connect()
            self._statuses[provider.provider_id] = ProviderStatus(
                provider_id=provider.provider_id,
                status="CONNECTED",
                last_health_check=datetime.datetime.utcnow().isoformat(),
                circuit_state="CLOSED"
            )
        except Exception as e:
            self._statuses[provider.provider_id] = ProviderStatus(
                provider_id=provider.provider_id,
                status="FAILED",
                last_health_check=datetime.datetime.utcnow().isoformat(),
                circuit_state="OPEN"
            )

    async def get_provider(self, provider_id: str) -> ToolProvider:
        if provider_id not in self._providers:
            raise KeyError(f"Provider {provider_id} not found")
        return self._providers[provider_id]

    async def monitor_health(self) -> None:
        for provider_id, provider in self._providers.items():
            try:
                status = await provider.health()
                self._statuses[provider_id].status = status
                self._statuses[provider_id].last_health_check = datetime.datetime.utcnow().isoformat()
            except Exception:
                self._statuses[provider_id].status = "UNHEALTHY"
                self._statuses[provider_id].last_health_check = datetime.datetime.utcnow().isoformat()

    async def list_providers(self) -> List[ToolProvider]:
        return list(self._providers.values())

    async def provider_status(self, provider_id: str) -> ProviderStatus:
        if provider_id not in self._statuses:
            raise KeyError(f"Provider {provider_id} status not found")
        return self._statuses[provider_id]

    async def refresh_capabilities(self) -> None:
        for provider_id, provider in self._providers.items():
            if self._statuses[provider_id].status == "CONNECTED":
                try:
                    tools = await provider.discover_tools()
                    # In a full implementation, we'd sync this with the ToolRegistry
                    self._statuses[provider_id].capabilities = [t.name for t in tools]
                except Exception:
                    pass
