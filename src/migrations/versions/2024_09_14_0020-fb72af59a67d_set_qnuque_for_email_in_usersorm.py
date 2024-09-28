"""Set qnuque for email in UsersORM

Revision ID: fb72af59a67d
Revises: c1162402402d
Create Date: 2024-09-14 00:20:35.934815

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "fb72af59a67d"
down_revision: Union[str, None] = "c1162402402d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
