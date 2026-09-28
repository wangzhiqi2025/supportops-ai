import logging
from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# 保存当前请求的 request_id
# ContextVar 可以让每个并发请求拥有自己独立的 request_id

# 支持并发隔离的变量
request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)

logger = logging.getLogger(__name__)


# 获取当前请求对应的 request_id
def get_request_id() -> str:
    return request_id_context.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    # 每个 HTTP 请求都会先经过这里
    async def dispatch(
        self,
        request: Request,
        # call_next= FastAPI 提供给你的“继续往后执行”的函数
        call_next,
    ) -> Response:
        # 优先使用客户端传入的 X-Request-ID
        # 如果没有，则自动生成一个新的 request_id
        request_id = request.headers.get("X-Request-ID") or uuid4().hex

        # 将 request_id 保存到当前请求上下文中
        # token 记住了“修改前的状态
        # token 的作用就是：记住 ContextVar 修改前的状态，方便请求结束后用 reset(token) 恢复。
        token = request_id_context.set(request_id)

        # 记录请求开始时间，用于计算耗时
        start_time = perf_counter()

        try:
            # 将请求继续交给后面的 Router / Service 处理
            response = await call_next(request)

            # 计算请求耗时，单位毫秒
            latency_ms = (perf_counter() - start_time) * 1000

            # 将 request_id 返回给客户端
            response.headers["X-Request-ID"] = request_id

            # 请求成功时记录日志
            logger.info(
                "request_completed",
                extra={
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "status_code": response.status_code,
                    "latency_ms": round(latency_ms, 2),
                },
            )

            return response

        except Exception:
            latency_ms = (perf_counter() - start_time) * 1000

            # 请求异常时记录异常堆栈和请求信息
            logger.exception(
                "request_failed",
                extra={
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "latency_ms": round(latency_ms, 2),
                },
            )

            # 继续向上抛出异常，交给全局异常处理器处理
            raise

        finally:
            # 请求结束后恢复 ContextVar，避免污染后续请求
            request_id_context.reset(token)
