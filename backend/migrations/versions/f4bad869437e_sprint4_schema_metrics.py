"""sprint4_schema_metrics

Revision ID: f4bad869437e
Revises: 8f10b7d34199
Create Date: 2026-06-24 23:53:22.061972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4bad869437e'
down_revision: Union[str, Sequence[str], None] = '8f10b7d34199'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('ai_extractions', 'confidence_score', new_column_name='overall_confidence')
    op.add_column('ai_extractions', sa.Column('contact_confidence', sa.Float(), nullable=True))
    op.add_column('ai_extractions', sa.Column('education_confidence', sa.Float(), nullable=True))
    op.add_column('ai_extractions', sa.Column('experience_confidence', sa.Float(), nullable=True))
    op.add_column('ai_extractions', sa.Column('skills_confidence', sa.Float(), nullable=True))
    op.add_column('ai_extractions', sa.Column('input_tokens', sa.Integer(), nullable=True))
    op.add_column('ai_extractions', sa.Column('output_tokens', sa.Integer(), nullable=True))
    op.add_column('ai_extractions', sa.Column('total_tokens', sa.Integer(), nullable=True))
    op.add_column('ai_extractions', sa.Column('processing_time_ms', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ai_extractions', 'processing_time_ms')
    op.drop_column('ai_extractions', 'total_tokens')
    op.drop_column('ai_extractions', 'output_tokens')
    op.drop_column('ai_extractions', 'input_tokens')
    op.drop_column('ai_extractions', 'skills_confidence')
    op.drop_column('ai_extractions', 'experience_confidence')
    op.drop_column('ai_extractions', 'education_confidence')
    op.drop_column('ai_extractions', 'contact_confidence')
    op.alter_column('ai_extractions', 'overall_confidence', new_column_name='confidence_score')
