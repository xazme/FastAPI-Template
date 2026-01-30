from fastapi import FastAPI, APIRouter
from .user.user_router import router as user_router
from .auth.auth_router import router as auth_router
from .kafka_demo.kafka_demo_router import router as kafka_demo_router


router = APIRouter()
router.include_router(
    router=auth_router,
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    router=user_router,
    prefix="/user",
    tags=["User"],
)
router.include_router(
    router=kafka_demo_router,
    prefix="/kafka",
    tags=["Kafka x FastStream"],
)


def init_routers(app: FastAPI):
    app.include_router(router=router)


__all__ = ["init_routers"]
