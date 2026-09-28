from typing import Any


# 应用层自定义异常
class AppError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = 400,
        details: Any | None = None,
    ) -> None:
        # 将 message 传给 Exception 父类
        super().__init__(message)

        # 业务错误码，例如 CHAT_UNAVAILABLE
        self.code = code

        # 对外返回的错误信息
        self.message = message

        # 对应的 HTTP 状态码
        self.status_code = status_code

        # 可选的额外错误详情
        self.details = details
