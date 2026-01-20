from fastapi import APIRouter

from users.views import user_router
from core.views import core_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(core_router)