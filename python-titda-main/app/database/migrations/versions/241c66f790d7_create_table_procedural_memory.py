"""create table procedural_memory

Revision ID: 241c66f790d7
Revises: bcd494d328c4
Create Date: 2023-05-27 11:03:01.033299

"""
from alembic import op
import sqlalchemy as sa

from database import ProceduralMemory

# revision identifiers, used by Alembic.
revision = '241c66f790d7'
down_revision = 'bcd494d328c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        ProceduralMemory.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("function_name", sa.String(255)),
        sa.Column("params", sa.JSON),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table(ProceduralMemory.__tablename__)
