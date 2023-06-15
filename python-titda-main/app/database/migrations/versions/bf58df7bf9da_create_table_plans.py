"""create table plans

Revision ID: bf58df7bf9da
Revises: 1ba399b49e62
Create Date: 2023-05-27 11:02:28.666485

"""
from alembic import op
import sqlalchemy as sa

from database import Plans

# revision identifiers, used by Alembic.
revision = 'bf58df7bf9da'
down_revision = '1ba399b49e62'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        Plans.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100)),
        sa.Column("description", sa.String(100)),
        sa.Column("level", sa.Enum("basic", "intermediate", "advanced"), default="basic"),
        sa.Column("goal_id", sa.Integer, nullable=True),
        sa.Column("discrepancy_id", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table(Plans.__tablename__)
