from fastapi import FastAPI

from supportops_ai.api.router import api_router
from supportops_ai.core.config import settings


# 创建并配置 FastAPI 应用
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )

    # 注册总路由，并统一添加 /api/v1 前缀
    app.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    return app


# 创建应用实例，供 Uvicorn 启动
app = create_app()