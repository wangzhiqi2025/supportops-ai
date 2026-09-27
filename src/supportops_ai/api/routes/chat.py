from fastapi import APIRouter

from supportops_ai.api.deps import ChatServiceDep
from supportops_ai.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    chat_service: ChatServiceDep,
) -> ChatResponse:
    return await chat_service.chat(request)
