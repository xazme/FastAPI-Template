from fastapi import APIRouter
from .user.user_router import router as user_router

router = APIRouter()
router.include_router(router=user_router, prefix="/user", tags=["User"])
__all__ = ["router"]


def main(): ...
