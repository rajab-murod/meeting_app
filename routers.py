from fastapi import APIRouter

from users.views import user_router
from core.edu_year_router import edu_year_router
from core.subject_router import subject_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(edu_year_router)
api_router.include_router(subject_router)