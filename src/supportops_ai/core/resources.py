from dataclasses import dataclass

import httpx

# 创建资源管理模块


@dataclass
class AppResources:
    http_client: httpx.AsyncClient
