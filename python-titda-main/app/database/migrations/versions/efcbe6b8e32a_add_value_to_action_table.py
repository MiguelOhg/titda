"""add value to action table

Revision ID: efcbe6b8e32a
Revises: ded975674025
Create Date: 2023-06-06 21:07:04.384989

"""
from alembic import op
import sqlalchemy as sa

from database import Actions

# revision identifiers, used by Alembic.
revision = 'efcbe6b8e32a'
down_revision = 'ded975674025'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(Actions.__tablename__, sa.Column("value", sa.String(100), nullable=True))
    op.add_column(Actions.__tablename__, sa.Column("type", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column(Actions.__tablename__, "value")
    op.drop_column(Actions.__tablename__, "type")
