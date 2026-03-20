"""add translation cache

Revision ID: a3f9c2e1b4d8
Revises: f80fda6d46f1
Create Date: 2026-03-20 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = 'a3f9c2e1b4d8'
down_revision: Union[str, None] = 'f80fda6d46f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'translation_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_hash', sa.String(length=64), nullable=False),
        sa.Column('source_text', sa.Text(), nullable=False),
        sa.Column('translated_text', sa.Text(), nullable=False),
        sa.Column('target_language', sa.String(length=10), nullable=False, server_default='pt'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_hash'),
    )
    op.create_index('ix_translation_cache_source_hash', 'translation_cache', ['source_hash'])


def downgrade() -> None:
    op.drop_index('ix_translation_cache_source_hash', table_name='translation_cache')
    op.drop_table('translation_cache')
