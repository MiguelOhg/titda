"""add status to perceptions table

Revision ID: 2432fc0b6648
Revises: d15aa9701820
Create Date: 2023-05-27 14:09:14.395170

"""
from alembic import op
import sqlalchemy as sa

from database import Perceptions

# revision identifiers, used by Alembic.
revision = '2432fc0b6648'
down_revision = 'd15aa9701820'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(Perceptions.__tablename__, sa.Column("status", sa.String(50)))


def downgrade() -> None:
    op.drop_column(Perceptions.__tablename__, "status")
