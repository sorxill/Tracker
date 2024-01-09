from fastapi import APIRouter

from .project import project_router
from .user import user_router

__all__ = [
    user_router,
    project_router,
]

router = APIRouter()
router.include_router(__all__)
