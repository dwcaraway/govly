"""add primary business email

Revision ID: 586551214149
Revises: 3b9b1a8230ba
Create Date: 2014-10-12 20:32:49.464478

"""

# revision identifiers, used by Alembic.
revision = '586551214149'
down_revision = '3b9b1a8230ba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('business', sa.Column('email', sa.String(400)))

def downgrade():
    op.drop_column('business', 'email')
