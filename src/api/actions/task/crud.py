from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.task import TaskCreate, TaskShow
from src.db.dals.task import TaskDAL
from src.db.models.task import Task


async def create_new_task(body: TaskCreate, session: AsyncSession) -> TaskShow:
    async with session.begin():
        task_dal = TaskDAL(session)
        task = await task_dal.dal_create_task(
            project_id=body.project,
            author_id=body.author,
            name=body.name,
            description=body.description,
            task_type=body.task_type,
            task_status=body.task_status,
            timestamp=body.timestamp,
        )
        return TaskShow(
            task_id=task.task_id,
            project_id=task.project_id,
            author_id=task.author_id,
            name=task.name,
            task_type=task.task_type,
            task_status=task.task_status,
            description=task.description,
            timestamp=task.timestamp,
        )


async def read_task_by_id(task_id: UUID, session: AsyncSession) -> Task | None:
    async with session.begin():
        task_dal = TaskDAL(session)
        task = await task_dal.dal_get_task_by_id(task_id)
        if task is not None:
            return task


async def delete_task(task_id: UUID, session: AsyncSession) -> UUID | None:
    async with session.begin():
        task_dal = TaskDAL(session)
        deleted_task_id = await task_dal.dal_delete_task(task_id)
        return deleted_task_id


async def update_task(
    updated_task_params: dict, task_id: UUID, session: AsyncSession
) -> Task | None:
    async with session.begin():
        task_dal = TaskDAL(session)
        updated_task = await task_dal.dal_update_task(task_id, **updated_task_params)
        return updated_task
