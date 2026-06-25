"""sprint3_schema

Revision ID: 8f10b7d34199
Revises: e0780876c1da
Create Date: 2026-06-24 23:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8f10b7d34199'
down_revision: Union[str, Sequence[str], None] = 'e0780876c1da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Alter jobstatus enum to add new values
    # PostgreSQL requires specific syntax to add enum values
    # For safety in this environment, we execute raw SQL to alter the enum if possible,
    # or just rely on the new python enum values if it's not strictly checked by the DB.
    # We will assume PostgreSQL 10+ syntax:
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'QUEUED';")
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'CANCELLED';")
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'RETRYING';")

    # 2. Make candidate_id nullable in candidate_documents
    op.alter_column('candidate_documents', 'candidate_id',
               existing_type=sa.UUID(),
               nullable=True)

    # 3. Create resume_ingestion_requests table
    op.create_table('resume_ingestion_requests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('document_id', sa.UUID(), nullable=False),
    sa.Column('job_id', sa.UUID(), nullable=True),
    sa.Column('status', postgresql.ENUM('PENDING', 'QUEUED', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'RETRYING', name='jobstatus', create_type=False), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['candidate_documents.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['job_id'], ['background_jobs.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resume_ingestion_requests_document_id'), 'resume_ingestion_requests', ['document_id'], unique=False)
    op.create_index(op.f('ix_resume_ingestion_requests_job_id'), 'resume_ingestion_requests', ['job_id'], unique=False)
    op.create_index(op.f('ix_resume_ingestion_requests_status'), 'resume_ingestion_requests', ['status'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_resume_ingestion_requests_status'), table_name='resume_ingestion_requests')
    op.drop_index(op.f('ix_resume_ingestion_requests_job_id'), table_name='resume_ingestion_requests')
    op.drop_index(op.f('ix_resume_ingestion_requests_document_id'), table_name='resume_ingestion_requests')
    op.drop_table('resume_ingestion_requests')

    op.alter_column('candidate_documents', 'candidate_id',
               existing_type=sa.UUID(),
               nullable=False)
