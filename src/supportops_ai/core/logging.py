import json
import logging
from datetime import UTC, datetime
from typing import Any

from supportops_ai.middleware.request_context import get_request_id


# 自定义 JSON 日志格式
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # 构造基础日志字段
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_request_id(),
        }

        # 这些字段可能通过 logger.info(..., extra={...}) 动态传入
        extra_fields = (
            "http_method",
            "http_path",
            "status_code",
            "latency_ms",
        )

        # 如果当前日志里存在这些额外字段，就加入 JSON 日志
        for field in extra_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)

        # 如果日志包含异常，则加入异常堆栈
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # 将字典转换成 JSON 字符串
        return json.dumps(
            log_data,
            ensure_ascii=False,
        )


# 配置整个应用的日志系统
def configure_logging(log_level: str = "INFO") -> None:
    # 日志输出到控制台
    handler = logging.StreamHandler()

    # 使用自定义的 JSON 日志格式
    handler.setFormatter(JsonFormatter())

    # 获取根 Logger，让整个项目统一使用这套日志配置
    root_logger = logging.getLogger()

    # 清除已有 Handler，避免重复输出日志
    root_logger.handlers.clear()

    # 添加控制台 Handler
    root_logger.addHandler(handler)

    # 设置日志级别
    root_logger.setLevel(log_level.upper())
