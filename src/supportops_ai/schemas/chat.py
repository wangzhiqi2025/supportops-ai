from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StringConstraints

MessageText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=4000,
    ),
]


class ChatRequest(BaseModel):
    message: MessageText
    session_id: UUID | None = None


class ChatResponse(BaseModel):
    session_id: UUID
    answer: str
