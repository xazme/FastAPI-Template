from fastapi import FastAPI, APIRouter
from .user.user_router import router as user_router

router = APIRouter()
router.include_router(router=user_router, prefix="/user", tags=["User"])


def init_routers(app: FastAPI):
    app.include_router(router=router)


__all__ = ["init_routers"]
