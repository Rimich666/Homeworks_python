"""empty message

Revision ID: bf2a1443766b
Revises: 6b081af88e54
Create Date: 2021-06-19 11:11:49.900329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf2a1443766b'
down_revision = '6b081af88e54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(length=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
