from fastapi import APIRouter

from supportops_ai.core.config import settings
from supportops_ai.schemas.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get(
    "",
    response_model=HealthResponse,
)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.app_env)
