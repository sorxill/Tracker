from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.task import Task


class TaskDAL:
    """Data Access Layer for operating task info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def dal_create_task(
        self,
        project_id: UUID,
        author_id: UUID,
        name: str,
        description: str,
        task_type: str,
        task_status: str,
        collaborators: UUID,
        **kwargs,
    ) -> Task:
        new_task = Task(
            project_id=project_id,
            author_id=author_id,
            name=name,
            description=description,
            task_type=task_type,
            task_status=task_status,
            collaborators=collaborators,
            timestamp=kwargs.get("timestamp"),
        )
        self.db_session.add(new_task)
        await self.db_session.commit()
        return new_task

    async def dal_get_task_by_id(self, task_id: UUID) -> Task | None:
        query = select(Task).where(Task.task_id == task_id)
        res = await self.db_session.execute(query)
        task_row = res.fetchone()
        if task_row is not None:
            return task_row[0]

    async def dal_update_task(self, task_id: UUID, **kwargs) -> Task | None:
        query = (
            update(Task).where(Task.task_id == task_id).values(kwargs).returning(Task)
        )
        res = await self.db_session.execute(query)
        updated_task_row = res.fetchone()
        if updated_task_row is not None:
            return updated_task_row[0]

    async def dal_delete_task(self, task_id: UUID) -> UUID | None:
        query = delete(Task).where(Task.task_id == task_id).returning(Task.task_id)
        res = await self.db_session.execute(query)
        deleted_task_id_row = res.fetchone()
        if deleted_task_id_row is not None:
            return deleted_task_id_row[0]

    async def dal_update_task_status(
        self, task_id: UUID, task_status: str
    ) -> Task | None:
        query = (
            update(Task)
            .where(Task.task_id == task_id)
            .values(task_status=task_status)
            .returning(Task)
        )
        res = await self.db_session.execute(query)
        updated_task_row = res.fetchone()
        if updated_task_row is not None:
            return updated_task_row[0]

    async def dal_get_task_by_author(self, author_id: UUID) -> Sequence[Task] | None:
        query = select(Task).where(Task.author_id == author_id).order_by(Task.timestamp)
        res = await self.db_session.execute(query)
        task_row = res.scalars().all()
        if task_row is None:
            return None
        return task_row
