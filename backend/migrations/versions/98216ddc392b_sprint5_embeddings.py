"""sprint5_embeddings

Revision ID: 98216ddc392b
Revises: e0780876c1da
Create Date: 2026-06-25 00:10:21.365313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '98216ddc392b'
down_revision: Union[str, None] = 'f4bad869437e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure vector extension exists
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')

    op.create_table('job_requirements',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('skills_required', sa.JSON(), nullable=False),
        sa.Column('experience_required', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('candidate_embeddings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('candidate_id', sa.UUID(), nullable=False),
        sa.Column('embedding_type', sa.String(length=50), nullable=False),
        sa.Column('embedding_model', sa.String(length=100), nullable=False),
        sa.Column('embedding_version', sa.String(length=50), nullable=False),
        sa.Column('source_hash', sa.String(length=255), nullable=False),
        sa.Column('vector_data', Vector(dim=1536), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_embeddings_candidate_id'), 'candidate_embeddings', ['candidate_id'], unique=False)
    op.create_index(op.f('ix_candidate_embeddings_embedding_type'), 'candidate_embeddings', ['embedding_type'], unique=False)
    op.create_index('idx_candidate_embeddings_vector', 'candidate_embeddings', ['vector_data'], postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'vector_data': 'vector_cosine_ops'})

    op.create_table('job_requirement_embeddings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('job_requirement_id', sa.UUID(), nullable=False),
        sa.Column('embedding_type', sa.String(length=50), nullable=False),
        sa.Column('embedding_model', sa.String(length=100), nullable=False),
        sa.Column('embedding_version', sa.String(length=50), nullable=False),
        sa.Column('source_hash', sa.String(length=255), nullable=False),
        sa.Column('vector_data', Vector(dim=1536), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['job_requirement_id'], ['job_requirements.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_requirement_embeddings_job_requirement_id'), 'job_requirement_embeddings', ['job_requirement_id'], unique=False)
    op.create_index(op.f('ix_job_requirement_embeddings_embedding_type'), 'job_requirement_embeddings', ['embedding_type'], unique=False)
    op.create_index('idx_job_requirement_embeddings_vector', 'job_requirement_embeddings', ['vector_data'], postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'vector_data': 'vector_cosine_ops'})


def downgrade() -> None:
    op.drop_table('job_requirement_embeddings')
    op.drop_table('candidate_embeddings')
    op.drop_table('job_requirements')
