"""rename user_name to username

Revision ID: a9e173ea39be
Revises: 219a5e26b597
Create Date: 2026-01-23 17:37:48.931428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9e173ea39be'
down_revision: Union[str, Sequence[str], None] = '219a5e26b597'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.alter_column("user", "user_name", new_column_name="username")


def downgrade() -> None:
    op.alter_column("user", "username", new_column_name="user_name")
