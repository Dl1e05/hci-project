from fastapi import APIRouter

from app.auth.api.v1.jwt_router import router as jwt_router
from app.auth.api.v1.router import router as auth_router
from app.references.api.v1.content_types_router import router as content_types_router
from app.references.api.v1.tags_router import router as tags_router
from app.users.api.v1.router import router as users_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(jwt_router)
main_router.include_router(users_router)
main_router.include_router(tags_router)
main_router.include_router(content_types_router)

__all__ = ['main_router']
