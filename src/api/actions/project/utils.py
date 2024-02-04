from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dals.project import ProjectDAL
from src.db.models import Project, ProjectCollaborators


async def get_projects_by_author(
    author_id: UUID,
    session: AsyncSession,
) -> Sequence[Project] | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        all_tasks = await project_dal.dal_get_projects_by_author(
            author_id,
        )
        return all_tasks


async def add_projects_contributor(
    project_id: UUID,
    contributor_id: UUID,
    session: AsyncSession,
) -> ProjectCollaborators | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        add_contributor = await project_dal.dal_add_projects_contributor(
            project_id,
            contributor_id,
        )
        return add_contributor


async def get_projects_contributor(
    project_id: UUID,
    contributor_id: UUID,
    session: AsyncSession,
) -> ProjectCollaborators | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        get_contributor = await project_dal.dal_get_projects_contributor(
            project_id,
            contributor_id,
        )
        return get_contributor


async def get_project_contributors(
    project_id: UUID,
    session: AsyncSession,
) -> Sequence[ProjectCollaborators] | None:
    async with session.begin():
        project_dal = ProjectDAL(session)
        all_contributors = await project_dal.dal_get_project_collaborators(
            project_id,
        )
        if all_contributors is not None:
            return all_contributors
