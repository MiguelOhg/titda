"""create table perceptions

Revision ID: 1ba399b49e62
Revises: 
Create Date: 2023-05-27 11:01:37.207940

"""
from alembic import op
import sqlalchemy as sa

from database import Perceptions

# revision identifiers, used by Alembic.
revision = '1ba399b49e62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        Perceptions.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("input", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table(Perceptions.__tablename__)
