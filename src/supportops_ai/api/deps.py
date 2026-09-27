from typing import Annotated

from fastapi import Depends

from supportops_ai.services.chat_service import ChatService


def get_chat_service() -> ChatService:
    return ChatService()


ChatServiceDep = Annotated[
    ChatService,
    Depends(get_chat_service),
]
