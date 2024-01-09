from fastapi import APIRouter

from .project import project_router
from .user import user_router

router = APIRouter()
router.include_router(project_router)
router.include_router(user_router)
