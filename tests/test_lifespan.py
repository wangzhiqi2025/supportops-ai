from fastapi.testclient import TestClient

from supportops_ai.main import app


def test_application_resources_are_initialized() -> None:
    # 使用上下文管理器启动 TestClient。
    # 进入 with 时会触发 FastAPI 的 lifespan/startup 逻辑，
    # 退出时会执行 shutdown 清理逻辑。
    with TestClient(app) as client:
        # 发起一次真实的应用级请求，确认应用能够正常启动并提供服务。
        response = client.get("/api/v1/health")

        assert response.status_code == 200

        # resources 应该在应用启动阶段被初始化，
        # 并保存到 app.state 中供后续依赖注入使用。
        resources = app.state.resources

        assert resources is not None

        # 验证共享 HTTP Client 已创建，
        # 防止后续 Service 调用外部接口时才发现资源未初始化。
        assert resources.http_client is not None
