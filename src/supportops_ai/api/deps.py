from typing import Annotated

from fastapi import Depends, Request

from supportops_ai.core.resources import AppResources
from supportops_ai.services.chat_service import ChatService

# api/deps.py 不负责“做业务”，负责“给 API 准备业务所需要的对象”。


def get_app_resources(request: Request) -> AppResources:
    return request.app.state.resources


AppResourcesDep = Annotated[
    AppResources,
    Depends(get_app_resources),
]


# 创建并返回一个 ChatService 实例
# FastAPI 会通过 Depends 调用这个函数来获取依赖对象
def get_chat_service(
    resources: AppResourcesDep,
) -> ChatService:
    return ChatService(
        resources=resources,
    )


# 定义 ChatService 的依赖注入类型别名
#
# Annotated 的含义：
# 1. 这个参数本身的类型是 ChatService
# 2. Depends(get_chat_service) 告诉 FastAPI：
#    不需要调用者手动传入 ChatService，
#    而是由 FastAPI 自动调用 get_chat_service() 获取
ChatServiceDep = Annotated[
    ChatService,
    Depends(get_chat_service),
]
