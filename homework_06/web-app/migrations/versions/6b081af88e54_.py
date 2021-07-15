"""empty message

Revision ID: 6b081af88e54
Revises: 408bc8bfcbdb
Create Date: 2021-06-19 11:10:14.073044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b081af88e54'
down_revision = '408bc8bfcbdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_phone_number_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_phone_number_key', 'users', ['phone_number'])
    # ### end Alembic commands ###
