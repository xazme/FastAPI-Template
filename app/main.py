import uvicorn
from app.config import settings


def main():
    """
    Start the Uvicorn ASGI server with application settings.

    This function runs the FastAPI application using Uvicorn with configuration
    values imported from the settings module. It allows for hot-reloading during
    development and supports multiple worker processes in production.

    The application is mounted from the module path 'app.server.server:app',
    where 'app' is the FastAPI instance. Host, port, reload mode, and number of
    workers are all configurable via the settings object.

    Example:
        >>> main()
        # Starts the server with settings defined in the settings module

    Note:
        This function should be called to start the web server when running
        the application. It does not return unless the server is stopped.
    """
    uvicorn.run(
        app="app.server.server:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.reload,
        workers=settings.workers,
    )


# find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
if __name__ == "__main__":
    main()
