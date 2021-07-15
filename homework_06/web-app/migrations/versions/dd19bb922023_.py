"""empty message

Revision ID: dd19bb922023
Revises: e53bd71cdc20
Create Date: 2021-06-15 18:25:32.139589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd19bb922023'
down_revision = 'e53bd71cdc20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.String(length=11), nullable=True),
    sa.Column('guid', sa.String(length=36), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('sum', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('bayer_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bayer_id'], ['buyers.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###
