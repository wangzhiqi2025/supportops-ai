import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from supportops_ai.core.exceptions import AppError
from supportops_ai.middleware.request_context import get_request_id
from supportops_ai.schemas.error import ErrorResponse

# 当前模块的 Logger
logger = logging.getLogger(__name__)


# 给 FastAPI 注册全局异常处理器
def register_exception_handlers(app: FastAPI) -> None:

    # 处理我们自己定义的业务异常 AppError
    @app.exception_handler(AppError)
    async def handle_app_error(
        request: Request,
        exc: AppError,
    ) -> JSONResponse:
        # 获取当前请求的 request_id
        request_id = get_request_id()

        # 记录业务异常日志
        logger.warning(
            "application_error",
            extra={
                "http_method": request.method,
                "http_path": request.url.path,
                "status_code": exc.status_code,
            },
        )

        # 构造统一错误响应
        error = ErrorResponse(
            code=exc.code,
            message=exc.message,
            request_id=request_id,
            details=exc.details,
        )

        # 返回 JSON HTTP 响应
        return JSONResponse(
            status_code=exc.status_code,
            content=error.model_dump(mode="json"),
            headers={
                "X-Request-ID": request_id,
            },
        )

    # 处理 FastAPI / Pydantic 参数校验异常
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        request_id = get_request_id()

        error = ErrorResponse(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            request_id=request_id,
            # exc.errors() 保存具体哪个字段校验失败
            details=exc.errors(),
        )

        return JSONResponse(
            status_code=422,
            content=error.model_dump(mode="json"),
            headers={
                "X-Request-ID": request_id,
            },
        )

    # 兜底处理所有没有被前面捕获的异常
    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        request_id = get_request_id()

        # logger.exception 会自动记录异常堆栈
        logger.exception(
            "unexpected_error",
            extra={
                "http_method": request.method,
                "http_path": request.url.path,
                "status_code": 500,
            },
        )

        # 不把真实异常内容暴露给客户端
        error = ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message="Internal server error.",
            request_id=request_id,
        )

        return JSONResponse(
            status_code=500,
            content=error.model_dump(mode="json"),
            headers={
                "X-Request-ID": request_id,
            },
        )
