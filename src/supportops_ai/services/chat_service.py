from uuid import uuid4

from supportops_ai.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    async def chat(self, request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or uuid4()

        return ChatResponse(
            session_id=session_id,
            answer=f"Received message: {request.message}",
        )
