import uvicorn
from app.config import settings


def main():
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
