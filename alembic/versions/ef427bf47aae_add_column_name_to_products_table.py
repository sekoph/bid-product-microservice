"""add column name to products table

Revision ID: ef427bf47aae
Revises: 74d0e3dd90f0
Create Date: 2024-10-18 20:15:37.163451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef427bf47aae'
down_revision: Union[str, None] = '74d0e3dd90f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('description', sa.String(length=255), nullable=False))


def downgrade() -> None:
    pass
