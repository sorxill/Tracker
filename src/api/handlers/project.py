from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.project.crud import (
    create_new_project,
    delete_project,
    read_project_by_id,
    read_project_by_name,
    update_project,
)
from src.api.schemas.project import (
    ProjectCreate,
    ProjectDelete,
    ProjectShow,
    ProjectUpdate,
)
from src.db.session import get_db

logger = getLogger(__name__)

project_router = APIRouter(prefix="/project")


@project_router.post("/create", response_model=ProjectShow)
async def create_project(body: ProjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_new_project(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@project_router.get("/read_by_name", response_model=ProjectShow)
async def get_project_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
):
    project = await read_project_by_name(name, db)
    if project is None:
        raise HTTPException(
            status_code=404, detail=f"Project with name '{name}' not found."
        )

    return project


@project_router.patch("/update", response_model=ProjectShow)
async def update_project_by_name(
    body: ProjectUpdate,
    name: str,
    db: AsyncSession = Depends(get_db),
):
    project_params = body.model_dump(exclude_none=True)
    if project_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_name = await read_project_by_name(name, db)
    if check_name is None:
        raise HTTPException(
            status_code=404, detail=f"Project with name '{name}' not found."
        )

    try:
        project_update = await update_project(name, db, project_params)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return project_update


@project_router.delete("/delete", response_model=ProjectDelete)
async def delete_project_by_id(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    check_id = await read_project_by_id(project_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found."
        )

    project_delete_id = await delete_project(project_id, db)
    if project_delete_id is None:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found."
        )
    return ProjectDelete(project_id=project_delete_id)
