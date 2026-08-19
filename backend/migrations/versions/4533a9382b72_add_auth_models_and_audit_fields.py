"""Add auth models and audit fields

Revision ID: 4533a9382b72
Revises: 417194ced827
Create Date: 2026-07-04 21:21:17.340230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4533a9382b72'
down_revision: Union[str, Sequence[str], None] = '417194ced827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
