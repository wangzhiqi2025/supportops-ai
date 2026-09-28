from fastapi.testclient import TestClient

from supportops_ai.main import app

client = TestClient(app)


def test_response_contains_request_id() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_existing_request_id_is_preserved() -> None:
    request_id = "test-request-id"

    response = client.get(
        "/api/v1/health",
        headers={
            "X-Request-ID": request_id,
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id
