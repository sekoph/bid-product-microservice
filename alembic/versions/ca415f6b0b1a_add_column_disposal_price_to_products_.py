"""add column disposal_price to products table

Revision ID: ca415f6b0b1a
Revises: fd09ac2d4c1e
Create Date: 2024-10-18 18:02:32.183180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca415f6b0b1a'
down_revision: Union[str, None] = 'fd09ac2d4c1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('disposal_price', sa.Float(), nullable=False))


def downgrade() -> None:
    pass
