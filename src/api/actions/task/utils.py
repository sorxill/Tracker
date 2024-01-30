from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dals.task import TaskDAL
from src.db.models.task import Task


async def update_task_status(
    task_id: UUID,
    task_status: str,
    session: AsyncSession,
) -> Task | None:
    async with session.begin():
        task_dal = TaskDAL(session)
        updated_task = await task_dal.dal_update_task_status(
            task_id,
            task_status,
        )
        return updated_task


async def get_tasks_by_author(
    author_id: UUID,
    session: AsyncSession,
) -> Sequence[Task] | None:
    async with session.begin():
        task_dal = TaskDAL(session)
        all_tasks = await task_dal.dal_get_task_by_author(
            author_id,
        )
        return all_tasks
