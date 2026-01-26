from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def init_cors_middleware(app: FastAPI) -> None:
    """
    Initialize and configure CORS (Cross-Origin Resource Sharing) middleware for the FastAPI application.

    This function adds the CORSMiddleware to the application, allowing controlled access
    to API resources from different origins. The configuration is based on settings
    defined in the settings module, enabling flexible and environment-specific policies.

    Args:
        app (FastAPI): The FastAPI application instance to which the middleware is added.

    Configuration:
        - allow_origins: List of allowed origins (e.g., "http://localhost:3000").
        - allow_credentials: Whether to allow cookies and credentials in cross-origin requests.
        - allow_methods: HTTP methods permitted (e.g., GET, POST, PUT, DELETE).
        - allow_headers: Headers that are allowed in cross-origin requests.

    Example:
        >>> init_cors_middleware(app)

    Note:
        This middleware is essential when the backend serves clients from different
        domains, such as single-page applications or mobile apps.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
