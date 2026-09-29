import pytest
from fastapi.testclient import TestClient

from supportops_ai.main import app


@pytest.fixture
def client():
    # 进入 TestClient 上下文时，会触发 FastAPI lifespan startup，
    # 从而初始化 app.state.resources。
    with TestClient(app) as test_client:
        yield test_client

    # 离开上下文后，会执行 lifespan shutdown，
    # 释放 HTTP Client 等应用级资源。