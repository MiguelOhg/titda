"""add_excercise_id_to_plans

Revision ID: b5cfbc456f7a
Revises: 2432fc0b6648
Create Date: 2023-05-30 22:38:14.013631

"""
from alembic import op
import sqlalchemy as sa

from database import Plans

# revision identifiers, used by Alembic.
revision = 'b5cfbc456f7a'
down_revision = '2432fc0b6648'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(Plans.__tablename__, sa.Column("exercise_id", sa.BigInteger, nullable=False))
    op.create_foreign_key("fk_plans_exercise_id", Plans.__tablename__, "mdl_vpl", ["exercise_id"], ["id"], onupdate='CASCADE', ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint("fk_plans_exercise_id", Plans.__tablename__, type_='foreignkey')
    op.drop_column(Plans.__tablename__, "exercise_id")
