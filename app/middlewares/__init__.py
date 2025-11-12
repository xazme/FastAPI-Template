from fastapi import FastAPI
from .cors_middleware import init_cors_middleware


def init_middlewares(app: FastAPI):
    init_cors_middleware(app=app)
    # and other middlewares


__all__ = ["init_middlewares"]
