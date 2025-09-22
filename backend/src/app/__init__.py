from fastapi import APIRouter

from app.auth.api.v1.jwt_router import router as jwt_router
from app.auth.api.v1.router import router as auth_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(jwt_router)

__all__ = ["main_router"]
