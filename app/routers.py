from fastapi import APIRouter

from users.views import user_router
from core.edu_year_router import edu_year_router
from core.subject_router import subject_router
from core.meeting_router import meeting_router
from core.issue_router import issue_router
from core.info_issue_router import info_issue_router
from core.att_router import att_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(edu_year_router)
api_router.include_router(subject_router)
api_router.include_router(meeting_router)
api_router.include_router(issue_router)
api_router.include_router(info_issue_router)
api_router.include_router(att_router)