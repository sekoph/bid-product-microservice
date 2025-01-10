"""create product category table

Revision ID: 5f17fa16a8f7
Revises: 
Create Date: 2024-10-18 15:02:45.148299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '5f17fa16a8f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product_category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('date_created', sa.DateTime(), default=datetime),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table("product_category")
