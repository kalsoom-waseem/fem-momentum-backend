"""remove userprofile table

Revision ID: ec57e29279e0
Revises: 1e7acfa97d54
Create Date: 2026-01-17 21:05:18.871881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec57e29279e0'
down_revision: Union[str, Sequence[str], None] = '1e7acfa97d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("userprofile")
    pass


def downgrade() -> None:
    op.create_table(
        "userprofile",
        # leave empty or reconstruct if you want rollback support
    )
    pass
