"""empty message

Revision ID: 548c2526258c
Revises: bf2a1443766b
Create Date: 2021-06-19 11:12:43.604658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '548c2526258c'
down_revision = 'bf2a1443766b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###