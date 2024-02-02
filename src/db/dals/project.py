from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.project import Project


class ProjectDAL:
    """Data Access Layer for operating project info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def dal_create_project(
        self,
        name: str,
        author_id: UUID,
        **kwargs,
    ) -> Project:
        new_project = Project(
            name=name,
            author_id=author_id,
            description=kwargs.get("description"),
        )
        self.db_session.add(new_project)
        await self.db_session.commit()
        return new_project

    async def dal_get_project_by_name(self, name: str) -> Project | None:
        query = select(Project).where(Project.name == name, Project.is_active)
        res = await self.db_session.execute(query)
        project_row = res.fetchone()
        if project_row is not None:
            return project_row[0]

    async def dal_get_project_by_id(self, project_id: UUID) -> Project | None:
        query = select(Project).where(
            Project.project_id == project_id, Project.is_active
        )
        res = await self.db_session.execute(query)
        project_row = res.fetchone()
        if project_row is not None:
            return project_row[0]

    async def dal_update_project(self, project_name: str, **kwargs) -> Project | None:
        query = (
            update(Project)
            .where(Project.name == project_name, Project.is_active)
            .values(kwargs)
            .returning(Project)
        )
        res = await self.db_session.execute(query)
        update_project_row = res.fetchone()
        if update_project_row is not None:
            return update_project_row[0]

    async def dal_delete_project(self, project_id: UUID) -> UUID | None:
        query = (
            update(Project)
            .where(Project.project_id == project_id, Project.is_active)
            .values(is_active=False)
            .returning(Project.project_id)
        )
        res = await self.db_session.execute(query)
        deleted_project_row = res.fetchone()
        if deleted_project_row is not None:
            return deleted_project_row[0]
