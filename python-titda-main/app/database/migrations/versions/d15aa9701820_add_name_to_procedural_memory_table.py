"""add name to procedural memory table

Revision ID: d15aa9701820
Revises: 95536d49e0d0
Create Date: 2023-05-27 12:18:17.797833

"""
from alembic import op
import sqlalchemy as sa

from database import ProceduralMemory

# revision identifiers, used by Alembic.
revision = 'd15aa9701820'
down_revision = '95536d49e0d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(ProceduralMemory.__tablename__, sa.Column("name", sa.String(50)))


def downgrade() -> None:
    op.drop_column(ProceduralMemory.__tablename__, "name")
