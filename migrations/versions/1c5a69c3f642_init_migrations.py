"""init_migrations

Revision ID: 1c5a69c3f642
Revises: 
Create Date: 2023-08-08 21:51:28.499324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c5a69c3f642'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer().with_variant(sa.Integer(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('category', sa.String(length=32), nullable=False, comment='카테고리'),
    sa.Column('price', sa.Integer(), nullable=False, comment='가격'),
    sa.Column('raw_price', sa.Integer(), nullable=False, comment='원가'),
    sa.Column('name', sa.String(length=64), nullable=False, comment='이름'),
    sa.Column('description', sa.String(length=512), nullable=False, comment='설명'),
    sa.Column('barcode', sa.String(length=128), nullable=False, comment='바코드'),
    sa.Column('size', sa.String(length=32), nullable=False, comment='사이즈 (small or large)'),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)
    op.create_table('user_tokens',
    sa.Column('id', sa.Integer().with_variant(sa.Integer(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(length=256), nullable=False, comment='액세스 토큰'),
    sa.Column('refresh_token', sa.String(length=256), nullable=False, comment='리프레시 토큰'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_tokens_user_id'), 'user_tokens', ['user_id'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer().with_variant(sa.Integer(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False, comment='핸드폰 번호'),
    sa.Column('password', sa.String(length=256), nullable=False, comment='비밀 번호'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_user_tokens_user_id'), table_name='user_tokens')
    op.drop_table('user_tokens')
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###
