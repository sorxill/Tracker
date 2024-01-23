from fastapi import APIRouter

from .login import login_router
from .project import project_router
from .task import task_router
from .user import user_router

routers = APIRouter(prefix="/api")
routers.include_router(project_router)
routers.include_router(user_router)
routers.include_router(login_router)
routers.include_router(task_router)
