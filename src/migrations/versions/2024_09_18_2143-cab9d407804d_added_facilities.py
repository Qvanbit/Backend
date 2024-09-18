"""added facilities

Revision ID: cab9d407804d
Revises: e6494773910a
Create Date: 2024-09-18 21:43:35.983757

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cab9d407804d"
down_revision: Union[str, None] = "e6494773910a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "room_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room__id", sa.BigInteger(), nullable=False),
        sa.Column("facility__id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility__id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room__id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("room_facilities")
    op.drop_table("facilities")
