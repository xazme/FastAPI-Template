from fastapi import FastAPI
from 


def _init_router(_app: FastAPI) -> None:
    from src.api import router

    _app.include_router(router=router)

def _init_middleware(_app: FastAPI) ->None:
