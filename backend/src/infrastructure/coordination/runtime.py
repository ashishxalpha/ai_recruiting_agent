from src.application.coordination.interfaces import CoordinationRuntime
from src.domain.coordination_models import CoordinationSession, CoordinationLifecycle

class DefaultCoordinationRuntime(CoordinationRuntime):
    async def start(self) -> CoordinationSession:
        return CoordinationSession(status=CoordinationLifecycle.RUNNING)

    async def pause(self) -> None:
        pass

    async def resume(self) -> None:
        pass

    async def cancel(self) -> None:
        pass

    async def status(self) -> str:
        return "RUNNING"
