"""add_thumbnail_to_project

Revision ID: add_thumbnail_001
Revises: 541102f8536d
Create Date: 2025-12-28 18:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_thumbnail_001'
down_revision: Union[str, None] = '541102f8536d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('projects', sa.Column('thumbnail_path', sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column('projects', 'thumbnail_path')
