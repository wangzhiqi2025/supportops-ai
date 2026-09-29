from uuid import uuid4

from supportops_ai.core.resources import AppResources
from supportops_ai.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(
        self,
        resources: AppResources,
    ) -> None:

        # "_"表示这是类内部使用的属性，外部最好不要直接访问。
        self._resources = resources

    async def chat(self, request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or uuid4()

        return ChatResponse(
            session_id=session_id,
            answer=f"Received message: {request.message}",
        )
