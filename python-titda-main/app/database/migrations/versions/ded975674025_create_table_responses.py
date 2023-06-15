"""create table responses

Revision ID: ded975674025
Revises: b5cfbc456f7a
Create Date: 2023-05-30 23:47:07.153900

"""
from alembic import op
import sqlalchemy as sa


from database import Response, Revision, Actions, ProceduralMemory


# revision identifiers, used by Alembic.
revision = 'ded975674025'
down_revision = 'b5cfbc456f7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        Response.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("exercise_id", sa.Integer),
        sa.Column("user_id", sa.Integer),
        sa.Column("archive_id", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        Revision.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("response_id", sa.Integer),
        sa.Column("action_id", sa.Integer),
        sa.Column("procedural_memory_id", sa.Integer),
        sa.Column("value", sa.String(255)),
        sa.Column("response_from_its", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_foreign_key("fk_revision_response_id", Revision.__tablename__, Response.__tablename__, ["response_id"], ["id"])
    op.create_foreign_key("fk_revision_action_id", Revision.__tablename__, Actions.__tablename__, ["action_id"], ["id"])
    op.create_foreign_key("fk_revision_discrepancy_id", Revision.__tablename__, ProceduralMemory.__tablename__, ["procedural_memory_id"],
                          ["id"])


def downgrade() -> None:
    op.drop_table(Response.__tablename__)
    op.drop_table(Revision.__tablename__)
