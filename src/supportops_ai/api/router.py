from fastapi import APIRouter

from supportops_ai.api.routes.chat import router as chat_router
from supportops_ai.api.routes.health import router as health_router

# 创建总路由
api_router = APIRouter()

# 注册各业务路由
api_router.include_router(health_router)
api_router.include_router(chat_router)