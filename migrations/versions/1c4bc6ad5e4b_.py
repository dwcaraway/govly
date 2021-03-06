"""empty message

Revision ID: 1c4bc6ad5e4b
Revises: 1d4f5e26ad39
Create Date: 2015-02-26 16:49:10.840907

"""

# revision identifiers, used by Alembic.
revision = '1c4bc6ad5e4b'
down_revision = '1d4f5e26ad39'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invitations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invitor_id', sa.Integer(), nullable=True),
    sa.Column('invitee_id', sa.Integer(), nullable=True),
    sa.Column('invitee_email', sa.String(length=128), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['invitee_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['invitor_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('invitee_email'),
    sa.UniqueConstraint('token')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invitations')
    ### end Alembic commands ###
