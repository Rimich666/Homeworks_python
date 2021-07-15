"""empty message

Revision ID: 3903ceb5013b
Revises: ab67193f73cf
Create Date: 2021-06-15 17:37:52.677716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3903ceb5013b'
down_revision = 'ab67193f73cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    # ### end Alembic commands ###
