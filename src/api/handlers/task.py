from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.task.crud import (
    create_new_task,
    delete_task,
    read_task_by_id,
    update_task,
)
from src.api.schemas.task import TaskCreate, TaskDelete, TaskShow, TaskUpdate
from src.db.session import get_db

logger = getLogger(__name__)

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.post("/create", response_model=TaskShow)
async def create_task(body: TaskCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_new_task(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@task_router.get("/read_by_id", response_model=TaskShow)
async def get_task_by_id(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    task = await read_task_by_id(task_id, db)
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with ID '{task_id}' not found."
        )

    return task


@task_router.patch("/update", response_model=TaskShow)
async def update_task_by_id(
    body: TaskUpdate,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    task_params = body.model_dump(exclude_none=True)
    if task_params == {}:
        raise HTTPException(status_code=422, detail="No parameters received")

    check_task = await read_task_by_id(task_id, db)
    if check_task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with ID '{task_id}' not found."
        )

    try:
        updated_task = await update_task(task_params, task_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_task


@task_router.delete("/delete", response_model=TaskDelete)
async def delete_task_by_id(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    deleted_task_id = await delete_task(task_id, db)
    if deleted_task_id is None:
        raise HTTPException(
            status_code=404, detail=f"Task with ID {task_id} not found."
        )
    return TaskDelete(task_id=deleted_task_id)
