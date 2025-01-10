"""create product table

Revision ID: fd09ac2d4c1e
Revises: 5f17fa16a8f7
Create Date: 2024-10-18 15:18:40.383361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'fd09ac2d4c1e'
down_revision: Union[str, None] = '5f17fa16a8f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(length=255), nullable=False),
        sa.Column('descriotion', sa.String(length=255), nullable=False, unique=True),
        sa.Column('location', sa.String(length=255), nullable=False, unique=True),
        sa.Column('is_closed', sa.Boolean(), default=False),
        sa.Column('file_name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('date_created', sa.DateTime(), default=datetime),
        sa.Column('product_category_id', sa.Integer),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    
    op.create_foreign_key('fk_product_category', 'products', 'product_category', ['product_category_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_table('products')
