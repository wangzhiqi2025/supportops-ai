from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 应用名称
    app_name: str = "SupportOps AI"

    # 当前运行环境，例如 development / test / production
    app_env: str = "development"

    # 是否开启调试模式
    debug: bool = False

    # API 统一版本前缀
    # 例如 /api/v1/health、/api/v1/chat
    api_v1_prefix: str = "/api/v1"

    # 配置 Pydantic Settings 的读取和解析规则
    model_config = SettingsConfigDict(
        # 从项目根目录下的 .env 文件读取环境变量
        env_file=".env",

        # .env 文件使用 UTF-8 编码
        env_file_encoding="utf-8",

        # 环境变量名称不区分大小写
        # 例如 API_V1_PREFIX 可以匹配 api_v1_prefix
        case_sensitive=False,

        # .env 中出现 Settings 未定义的额外字段时直接忽略
        extra="ignore",
    )


# 缓存 Settings 对象，避免每次调用都重新创建和读取配置
@lru_cache
def get_settings() -> Settings:
    return Settings()


# 创建全局配置对象，项目其他模块可以直接导入使用
settings = get_settings()