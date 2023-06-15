"""create table actions

Revision ID: 204f9519ea5a
Revises: bf58df7bf9da
Create Date: 2023-05-27 11:02:32.829347

"""
from alembic import op
import sqlalchemy as sa

from database import Actions, Plans

# revision identifiers, used by Alembic.
revision = '204f9519ea5a'
down_revision = 'bf58df7bf9da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        Actions.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100)),
        sa.Column("description", sa.String(100)),
        sa.Column("plan_id", sa.Integer),
        sa.Column("procedural_memory_id", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_foreign_key("fk_action_plan_id", Actions.__tablename__, Plans.__tablename__, ["plan_id"], ["id"])


def downgrade() -> None:
    op.drop_table(Actions.__tablename__)
