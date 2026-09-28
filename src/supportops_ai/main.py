from fastapi import FastAPI

from supportops_ai.api.router import api_router
from supportops_ai.core.config import settings
from supportops_ai.core.exception_handlers import register_exception_handlers
from supportops_ai.core.logging import configure_logging
from supportops_ai.middleware.request_context import RequestContextMiddleware


def create_app() -> FastAPI:
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )

    app.add_middleware(RequestContextMiddleware)

    register_exception_handlers(app)

    app.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    return app


app = create_app()
