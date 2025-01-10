"""alter column name to products table

Revision ID: 74d0e3dd90f0
Revises: ca415f6b0b1a
Create Date: 2024-10-18 19:47:33.882586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74d0e3dd90f0'
down_revision: Union[str, None] = 'ca415f6b0b1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('products', 'descriotion')


def downgrade() -> None:
    pass
