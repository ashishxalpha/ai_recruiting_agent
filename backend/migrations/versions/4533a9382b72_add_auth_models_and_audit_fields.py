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
    # Create role enum
    op.execute("CREATE TYPE role AS ENUM ('ADMIN', 'RECRUITER', 'HIRING_MANAGER', 'VIEWER', 'SYSTEM')")
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'RECRUITER', 'HIRING_MANAGER', 'VIEWER', 'SYSTEM', name='role'), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.UUID(as_uuid=True), nullable=True)
    )

    # Create user_sessions
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('refresh_token_hash', sa.String(512), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(512), nullable=True),
        sa.Column('is_revoked', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', sa.UUID(as_uuid=True), nullable=True)
    )

    # Create password_reset_tokens
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('token_hash', sa.String(512), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_used', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('updated_by', sa.UUID(as_uuid=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('password_reset_tokens')
    op.drop_table('user_sessions')
    op.drop_table('users')
    op.execute("DROP TYPE role")
