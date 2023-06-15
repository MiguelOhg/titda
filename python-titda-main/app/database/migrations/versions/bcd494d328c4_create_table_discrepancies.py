"""create table discrepancies

Revision ID: bcd494d328c4
Revises: 5aef2e30d9c6
Create Date: 2023-05-27 11:02:43.931000

"""
from alembic import op
import sqlalchemy as sa

from database import Discrepancy, Plans

# revision identifiers, used by Alembic.
revision = 'bcd494d328c4'
down_revision = '5aef2e30d9c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        Discrepancy.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("description", sa.String(255)),
        sa.Column("plan_id", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_foreign_key("fk_discrepancy_plan_id", Discrepancy.__tablename__, Plans.__tablename__, ["plan_id"], ["id"])


def downgrade() -> None:
    op.drop_table(Discrepancy.__tablename__)
