"""version1

Revision ID: 938870a56f6d
Revises: 
Create Date: 2023-11-10 18:34:17.356444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '938870a56f6d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.String(length=256), nullable=False),
    sa.Column('product_code', sa.String(length=256), nullable=False),
    sa.Column('customer_fullname', sa.String(length=256), nullable=True),
    sa.Column('product_name', sa.String(length=256), nullable=True),
    sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###