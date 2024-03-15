"""
Project Handlers
"""

from logging import getLogger
from typing import List
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
from src.api.actions.project.utils import (
    add_projects_contributor,
    get_project_contributors,
    get_projects_by_author,
    get_projects_contributor,
)
from src.api.actions.user.crud import read_user_by_id
from src.api.handlers.login import auth_check_user_info
from src.api.schemas.project import (
    ProjectAddContributor,
    ProjectCreate,
    ProjectDelete,
    ProjectShow,
    ProjectUpdate,
)
from src.api.schemas.user import UserForToken
from src.db.session import get_db

logger = getLogger(__name__)

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.post("/create", response_model=ProjectShow)
async def create_project(
    body: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to create a new project
    """

    try:
        return await create_new_project(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@project_router.get("/read_by_name", response_model=ProjectShow)
async def get_project_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to get the project info by name
    """

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
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to update a project params by project name
    Necessary to het some params
    """

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
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to delete a project by uuid
    """

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


@project_router.get("/{author_id}/all_projects", response_model=List[ProjectShow])
async def get_task_by_author_all(
    author_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to get all projects by author id
    """

    check_id = await read_user_by_id(author_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {author_id} not found."
        )

    projects = await get_projects_by_author(
        author_id,
        db,
    )
    if projects is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id {author_id} don't have projects.",
        )
    return projects


@project_router.post("/add_contributor", response_model=ProjectAddContributor)
async def add_contributor(
    project_id: UUID,
    contributor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to add a contributor to a project by contributor id
    """

    check_user_id = await read_user_by_id(
        contributor_id,
        db,
    )
    if check_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {contributor_id} not found."
        )

    check_project_id = await read_project_by_id(
        project_id,
        db,
    )
    if check_project_id is None:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found."
        )

    check_contributor_exist = await get_projects_contributor(
        project_id,
        contributor_id,
        db,
    )
    if check_contributor_exist is not None:
        raise HTTPException(
            status_code=404,
            detail=f"Contributor with id {contributor_id} already exists.",
        )

    try:
        return await add_projects_contributor(
            project_id=project_id,
            contributor_id=contributor_id,
            session=db,
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@project_router.get(
    "/{project_id}/contributors", response_model=List[ProjectAddContributor]
)
async def get_project_all_contributors(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to get all contributors from this project
    """

    check_project_id = await read_project_by_id(project_id, db)
    if check_project_id is None:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found."
        )
    contributors = await get_project_contributors(
        project_id,
        db,
    )
    if contributors is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with id {project_id} has no one contributor.",
        )
    return contributors
