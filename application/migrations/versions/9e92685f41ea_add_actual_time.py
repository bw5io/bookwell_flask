"""add actual time

Revision ID: 9e92685f41ea
Revises: 2d8f2be349e5
Create Date: 2022-01-01 15:34:01.094297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e92685f41ea'
down_revision = '2d8f2be349e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meeting', sa.Column('actualTime', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meeting', 'actualTime')
    # ### end Alembic commands ###
