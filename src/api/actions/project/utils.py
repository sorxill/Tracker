# from typing import Sequence
# from uuid import UUID
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.db.dals.project import ProjectDAL
# from src.db.models import Project
#

# async def get_projects_by_author(
#     author_id: UUID,
#     session: AsyncSession,
# ) -> Sequence[Project] | None:
#     async with session.begin():
#         project_dal = ProjectDAL(session)
#         all_tasks = await project_dal.dal_get_project_by_name(
#             author_id,
#             session,
#         )
#         return all_tasks
