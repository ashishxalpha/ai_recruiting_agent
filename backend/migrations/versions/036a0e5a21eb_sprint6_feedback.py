"""sprint6_feedback

Revision ID: 036a0e5a21eb
Revises: 98216ddc392b
Create Date: 2026-06-25 16:21:42.061972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '036a0e5a21eb'
down_revision: Union[str, None] = '98216ddc392b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # search_sessions table
    op.create_table('search_sessions',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('job_requirement_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['job_requirement_id'], ['job_requirements.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_search_sessions_job_requirement_id'), 'search_sessions', ['job_requirement_id'], unique=False)

    # candidate_matches table
    op.create_table('candidate_matches',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('search_session_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('semantic_score', sa.Float(), nullable=False),
        sa.Column('skills_score', sa.Float(), nullable=False),
        sa.Column('experience_score', sa.Float(), nullable=False),
        sa.Column('education_score', sa.Float(), nullable=False),
        sa.Column('quality_score', sa.Float(), nullable=False),
        sa.Column('final_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['search_session_id'], ['search_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_matches_search_session_id'), 'candidate_matches', ['search_session_id'], unique=False)
    op.create_index(op.f('ix_candidate_matches_candidate_id'), 'candidate_matches', ['candidate_id'], unique=False)
    op.create_index(op.f('ix_candidate_matches_final_score'), 'candidate_matches', ['final_score'], unique=False)

    # match_explanations table
    op.create_table('match_explanations',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_match_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('explanation_version', sa.String(length=50), nullable=False),
        sa.Column('strengths', sa.JSON(), nullable=False),
        sa.Column('gaps', sa.JSON(), nullable=False),
        sa.Column('recommendations', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['candidate_match_id'], ['candidate_matches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_match_id')
    )

    # recruiter_feedback table
    op.create_table('recruiter_feedback',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_match_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('decision', sa.String(length=50), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['candidate_match_id'], ['candidate_matches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recruiter_feedback_candidate_match_id'), 'recruiter_feedback', ['candidate_match_id'], unique=False)

    # ground_truth_events table
    op.create_table('ground_truth_events',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('job_requirement_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('ai_score', sa.Float(), nullable=False),
        sa.Column('recruiter_decision', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['job_requirement_id'], ['job_requirements.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ground_truth_events_candidate_id'), 'ground_truth_events', ['candidate_id'], unique=False)
    op.create_index(op.f('ix_ground_truth_events_job_requirement_id'), 'ground_truth_events', ['job_requirement_id'], unique=False)


def downgrade() -> None:
    op.drop_table('ground_truth_events')
    op.drop_table('recruiter_feedback')
    op.drop_table('match_explanations')
    op.drop_table('candidate_matches')
    op.drop_table('search_sessions')
