"""create table goals

Revision ID: 5aef2e30d9c6
Revises: 204f9519ea5a
Create Date: 2023-05-27 11:02:36.681094

"""
from alembic import op
import sqlalchemy as sa

from database import Goal, Plans

# revision identifiers, used by Alembic.
revision = '5aef2e30d9c6'
down_revision = '204f9519ea5a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        Goal.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100)),
        sa.Column("description", sa.String(100)),
        sa.Column("plan_id", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_foreign_key("fk_goal_plan_id", Goal.__tablename__, Plans.__tablename__, ["plan_id"], ["id"])


def downgrade() -> None:
    op.drop_table(Goal.__tablename__)
