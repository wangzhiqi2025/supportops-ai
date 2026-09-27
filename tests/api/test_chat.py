from fastapi.testclient import TestClient

from supportops_ai.main import app

client = TestClient(app)


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
