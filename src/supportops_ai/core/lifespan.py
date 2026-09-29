import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from supportops_ai.core.config import settings
from supportops_ai.core.resources import AppResources

# 当前模块的 Logger
logger = logging.getLogger(__name__)


# 管理 FastAPI 应用的启动和关闭生命周期
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("application_starting")

    # 创建应用级共享 HTTP Client
    # 整个应用运行期间复用同一个连接池
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(settings.http_timeout_seconds),
        limits=httpx.Limits(
            max_connections=settings.http_max_connections,
            max_keepalive_connections=settings.http_max_keepalive_connections,
        ),
    )

    # 将共享资源挂载到 app.state，供后续依赖注入使用
    app.state.resources = AppResources(
        http_client=http_client,
    )

    logger.info("application_started")

    try:
        # yield 前：应用启动阶段
        # yield 期间：FastAPI 正常运行
        # yield 后：进入应用关闭阶段
        yield

    finally:
        logger.info("application_stopping")

        # 应用关闭时释放 HTTP Client 及其连接池资源
        await http_client.aclose()

        logger.info("application_stopped")
