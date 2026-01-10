from fastapi import FastAPI
from app.config import settings
from app.api import init_routers
from app.middlewares import init_middlewares
from app.exception_handlers import init_exception_handlers
from .lifespan import app_lifespan


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    This function initializes a FastAPI application with metadata such as title,
    description, and version. It sets up the application lifespan handler for
    managing startup and shutdown events, and configures documentation endpoints
    based on settings.

    Additionally, it registers middlewares, routers, and exception handlers
    necessary for the application to function.

    Returns:
        FastAPI: A fully configured FastAPI application instance ready to be served.

    Example:
        >>> app = create_app()
        >>> uvicorn.run(app, host="0.0.0.0", port=8000)

    Note:
        The documentation UI (Swagger UI and ReDoc) URLs are configurable via
        the settings module to allow enabling or disabling in different environments.
    """
    app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=app_lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    init_middlewares(app=app)
    init_routers(app=app)
    init_exception_handlers(app=app)
    return app


app = create_app()
