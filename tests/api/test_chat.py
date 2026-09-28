from fastapi.testclient import TestClient

from supportops_ai.api.deps import get_chat_service
from supportops_ai.core.exceptions import AppError
from supportops_ai.main import app
from supportops_ai.schemas.chat import ChatRequest, ChatResponse
from supportops_ai.services.chat_service import ChatService

client = TestClient(app)


class FailingChatService(ChatService):
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        raise AppError(
            code="CHAT_UNAVAILABLE",
            message="Chat service is temporarily unavailable.",
            status_code=503,
        )


def test_chat_success() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Docker Desktop cannot start.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert data["answer"] == "Received message: Docker Desktop cannot start."


def test_chat_rejects_empty_message() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["code"] == "VALIDATION_ERROR"
    assert data["message"] == "Request validation failed."
    assert "request_id" in data


def test_chat_strips_message_whitespace() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "   Docker error   ",
        },
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Received message: Docker error"


def test_chat_preserves_session_id() -> None:
    session_id = "550e8400-e29b-41d4-a716-446655440000"

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Continue our previous conversation.",
            "session_id": session_id,
        },
    )

    assert response.status_code == 200
    assert response.json()["session_id"] == session_id


def test_chat_handles_application_error() -> None:
    app.dependency_overrides[get_chat_service] = lambda: FailingChatService()

    try:
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Hello",
            },
        )

        assert response.status_code == 503

        data = response.json()

        assert data["code"] == "CHAT_UNAVAILABLE"
        assert data["message"] == "Chat service is temporarily unavailable."
        assert "request_id" in data

    finally:
        app.dependency_overrides.clear()
