"""delete_projects_users_db

Revision ID: c8780ace4baf
Revises: 2cb061bd0acc
Create Date: 2024-01-27 20:57:40.919402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8780ace4baf'
down_revision: Union[str, None] = '2cb061bd0acc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects_users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects_users',
    sa.Column('project_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], name='projects_users_project_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='projects_users_user_id_fkey'),
    sa.PrimaryKeyConstraint('project_id', 'user_id', name='projects_users_pkey')
    )
    # ### end Alembic commands ###