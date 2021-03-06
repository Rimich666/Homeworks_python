"""empty message

Revision ID: 811f25d955f8
Revises: 
Create Date: 2021-07-25 13:53:41.563242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '811f25d955f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kode', sa.Integer(), nullable=False),
    sa.Column('buyer_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kode')
    )
    op.create_table('prices_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pt_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pt_name')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('kode', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kode'),
    sa.UniqueConstraint('product_name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role')
    )
    op.create_table('prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('pt_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['pt_id'], ['prices_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_id', 'pt_id', 'date', name='price_uk')
    )
    op.create_index(op.f('ix_prices_date'), 'prices', ['date'], unique=False)
    op.create_table('shops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kode', sa.String(length=8), nullable=False),
    sa.Column('shop_name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('pt_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyers.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['pt_id'], ['prices_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('buyer_id', 'kode')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.String(length=11), nullable=True),
    sa.Column('guid', sa.String(length=36), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('sum', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyers.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guid')
    )
    op.create_table('territory',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('orders_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Numeric(precision=14, scale=3), nullable=False),
    sa.Column('sum', sa.Numeric(precision=15, scale=2), nullable=False),
    sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_products')
    op.drop_table('territory')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('shops')
    op.drop_index(op.f('ix_prices_date'), table_name='prices')
    op.drop_table('prices')
    op.drop_table('roles')
    op.drop_table('products')
    op.drop_table('prices_type')
    op.drop_table('buyers')
    # ### end Alembic commands ###
