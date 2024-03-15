"""
Task Handlers
"""

from logging import getLogger
from typing import List
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
from src.api.actions.task.utils import get_tasks_by_author, update_task_status
from src.api.actions.user.crud import read_user_by_id
from src.api.handlers.login import auth_check_user_info
from src.api.schemas.task import (
    TaskCreate,
    TaskDelete,
    TaskShow,
    TaskUpdate,
    TaskUpdateStatus,
)
from src.api.schemas.user import UserForToken
from src.db.session import get_db

logger = getLogger(__name__)

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.post("/create", response_model=TaskShow)
async def create_task(
    body: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to create a new task
    """

    try:
        return await create_new_task(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}",
        ) from err


@task_router.get("/read_by_id", response_model=TaskShow)
async def get_task_by_id(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to get the task info by uuid
    """

    task = await read_task_by_id(task_id, db)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found.",
        )

    return task


@task_router.patch("/update", response_model=TaskShow)
async def update_task_by_id(
    body: TaskUpdate,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to update a task params by user id
    Necessary to het some params
    """

    task_params = body.model_dump(exclude_none=True)
    if task_params == {}:
        raise HTTPException(
            status_code=422,
            detail="No one parameters get.",
        )

    check_task = await read_task_by_id(task_id, db)
    if check_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found.",
        )

    try:
        updated_task = await update_task(task_params, task_id, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}",
        ) from err
    return updated_task


@task_router.delete("/delete", response_model=TaskDelete)
async def delete_task_by_id(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to delete a task by uuid
    """

    deleted_task_id = await delete_task(task_id, db)
    if deleted_task_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found.",
        )
    return TaskDelete(task_id=deleted_task_id)


@task_router.patch("/update_status", response_model=TaskShow)
async def update_task_status_by_id(
    body: TaskUpdateStatus,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to update task status
    """

    task_status = body.task_status

    check_task = await read_task_by_id(task_id, db)
    if check_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found.",
        )

    try:
        updated_task = await update_task_status(task_id, task_status, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}",
        ) from err
    return updated_task


@task_router.get("/read_all_by_author", response_model=List[TaskShow])
async def get_task_by_author_all(
    author_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    """
    Handler to get all tasks for a given user
    Which is task author
    """

    check_id = await read_user_by_id(author_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {author_id} not found.",
        )

    tasks = await get_tasks_by_author(
        author_id,
        db,
    )
    if tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id {author_id} don't have tasks.",
        )

    return tasks
