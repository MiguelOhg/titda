"""create table relations

Revision ID: 95536d49e0d0
Revises: 241c66f790d7
Create Date: 2023-05-27 11:03:05.775002

"""
from alembic import op

from database import Plans, Goal, Discrepancy, Actions, ProceduralMemory

# revision identifiers, used by Alembic.
revision = '95536d49e0d0'
down_revision = '241c66f790d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key("fk_plan_goal_id", Plans.__tablename__, Goal.__tablename__, ["goal_id"], ["id"])
    op.create_foreign_key("fk_plan_discrepancy_id", Plans.__tablename__, Discrepancy.__tablename__, ["discrepancy_id"], ["id"])
    op.create_foreign_key("fk_action_procedural_memory_id", Actions.__tablename__, ProceduralMemory.__tablename__, ["procedural_memory_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("fk_plan_goal_id", Plans.__tablename__, type_='foreignkey')
    op.drop_constraint("fk_plan_discrepancy_id", Plans.__tablename__, type_='foreignkey')
    op.drop_constraint("fk_action_procedural_memory_id", Actions.__tablename__, type_='foreignkey')
