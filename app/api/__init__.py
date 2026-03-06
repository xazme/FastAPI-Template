from fastapi import APIRouter, FastAPI
from faststream.kafka import KafkaBroker

from .auth.auth_router import router as auth_router
from .user.user_router import router as user_router

# from .auth.auth_consumer import router as auth_consumer_router

router = APIRouter(prefix="/api")

router.include_router(
    router=auth_router,
    prefix="/auth-service",
    tags=["Auth"],
)
router.include_router(
    router=user_router,
    prefix="/user-service",
    tags=["User"],
)


def init_routers(
    app: FastAPI,
) -> None:
    app.include_router(router=router)


def init_consumers(
    broker: KafkaBroker,
) -> None:
    # broker.include_router(router=user_consumer_router)
    pass


__all__ = [
    "init_consumers",
    "init_routers",
]
