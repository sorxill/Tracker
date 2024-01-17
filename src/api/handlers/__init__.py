from fastapi import APIRouter

from .login import login_router
from .project import project_router
from .user import user_router

routers = APIRouter()
routers.include_router(project_router)
routers.include_router(user_router)
