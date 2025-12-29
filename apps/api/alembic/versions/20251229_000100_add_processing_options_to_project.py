"""Add processing_options to project

Revision ID: add_processing_options
Revises: add_thumbnail_to_project
Create Date: 2025-12-29 00:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'add_processing_options'
down_revision: Union[str, None] = 'add_thumbnail_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('projects', sa.Column('processing_options', JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column('projects', 'processing_options')
