"""TimeSlots

Revision ID: a018a0a153ed
Revises: 0e74715d2e0b
Create Date: 2021-12-28 16:13:01.153868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a018a0a153ed'
down_revision = '0e74715d2e0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meeting_joiners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('meeting', sa.Integer(), nullable=False),
    sa.Column('student', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meeting'], ['meeting.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meeting_slots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('meeting', sa.Integer(), nullable=False),
    sa.Column('timeslot', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meeting'], ['meeting.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['timeslot'], ['time_slot_inventory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('time_slot_inventory', sa.Column('occupied', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('time_slot_inventory', 'occupied')
    op.drop_table('meeting_slots')
    op.drop_table('meeting_joiners')
    # ### end Alembic commands ###
