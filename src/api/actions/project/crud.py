"""
Project Actions
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.project import ProjectCreate, ProjectShow
from src.db.dals.project import ProjectDAL
from src.db.models.project import Project


async def create_new_project(body: ProjectCreate, session: AsyncSession) -> ProjectShow:
    """
    Action to create a new project
    """

    async with session.begin():
        project_dal = ProjectDAL(session)
        project = await project_dal.dal_create_project(
            name=body.name,
            author_id=body.author_id,
            description=body.description,
        )
        return ProjectShow(
            name=project.name,
            description=project.description,
            author_id=project.author_id,
            project_id=project.project_id,
            is_active=project.is_active,
        )


async def read_project_by_name(name: str, session: AsyncSession) -> Project | None:
    """
    Action to get the project by name
    """

    async with session.begin():
        project_dal = ProjectDAL(session)
        project = await project_dal.dal_get_project_by_name(name)
        if project is not None:
            return project


async def read_project_by_id(project_id: UUID, session: AsyncSession) -> Project | None:
    """
    Action to get project by uuid
    """

    async with session.begin():
        project_dal = ProjectDAL(session)
        project = await project_dal.dal_get_project_by_id(project_id)
        if project is not None:
            return project


async def delete_project(project_id, session) -> UUID | None:
    """
    Action to delete project by project uuid
    """

    async with session.begin():
        project_dal = ProjectDAL(session)
        deleted_project_id = await project_dal.dal_delete_project(
            project_id=project_id,
        )
        return deleted_project_id


async def update_project(
    project_name: str,
    session,
    updated_project_params: dict,
) -> Project | None:
    """
    Action to update project params by project name
    """

    async with session.begin():
        project_dal = ProjectDAL(session)
        updated_project = await project_dal.dal_update_project(
            project_name=project_name, **updated_project_params
        )
        return updated_project
