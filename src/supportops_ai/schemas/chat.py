from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StringConstraints

# 定义一个“带约束的字符串类型”
#
# 本质上它还是 str，
# 只是额外增加了下面这些校验规则：
#
# strip_whitespace=True
#   自动去掉字符串两端的空格
#
# min_length=1
#   最少必须有 1 个字符
#   也就是说不能传空字符串
#
# max_length=4000
#   最多允许 4000 个字符
#
# 所以 MessageText 可以理解成：
# “一个经过 Pydantic 校验的消息字符串”
MessageText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=4000,
    ),
]


# 定义聊天接口的“请求数据结构”
#
# BaseModel 表示这是一个 Pydantic 数据模型，
# FastAPI 收到请求后会自动按照这个模型校验数据
class ChatRequest(BaseModel):
    # 用户发送的聊天内容
    #
    # 类型不是普通 str，
    # 而是上面定义的 MessageText，
    # 所以会自动进行：
    # - 去除首尾空格
    # - 非空校验
    # - 最大长度 4000 校验
    message: MessageText

    # 当前会话 ID
    #
    # UUID：
    #   表示必须是合法的 UUID
    #
    # | None：
    #   表示也允许没有 session_id
    #
    # = None：
    #   表示如果用户没传，默认值就是 None
    session_id: UUID | None = None


# 定义聊天接口的“响应数据结构”
class ChatResponse(BaseModel):
    # 返回当前会话的唯一 ID
    #
    # 如果请求中已经有 session_id，
    # 通常继续返回原来的 session_id；
    #
    # 如果请求中没有，
    # 服务端可以创建一个新的 UUID
    session_id: UUID

    # AI 最终生成的回答
    answer: str
