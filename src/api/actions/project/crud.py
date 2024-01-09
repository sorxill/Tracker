from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.project import ProjectCreate, ProjectShow
from src.db.dals.project import ProjectDAL
from src.db.models.project import Project


async def create_new_project(body: ProjectCreate, session: AsyncSession) -> ProjectShow:
    async with session.begin():
        project_dal = ProjectDAL(session)
        project = await project_dal.dal_create_project(
            name=body.name,
            author=body.author,
            description=body.description,
        )
        return ProjectShow(
            name=project.name,
            description=project.description,
            author=project.author,
            project_id=project.project_id,
            is_active=project.is_active,
        )


async def read_project_by_name(name: str, session: AsyncSession) -> Project | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        project = await project_dal.dal_get_project_by_name(name)
        if project is not None:
            return project


async def delete_project(project_id, session) -> UUID | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        deleted_project_id = await project_dal.dal_delete_project(
            project_id=project_id,
        )
        return deleted_project_id


async def update_project(
    updated_project_params: dict, project_id: UUID, session
) -> Project | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        updated_project = await project_dal.dal_update_project(
            project_id=project_id, **updated_project_params
        )
        return updated_project
