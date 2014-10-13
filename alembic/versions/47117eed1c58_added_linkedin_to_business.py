"""added linkedin to business

Revision ID: 47117eed1c58
Revises: 586551214149
Create Date: 2014-10-13 10:26:03.180917

"""

# revision identifiers, used by Alembic.
revision = '47117eed1c58'
down_revision = '586551214149'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('business', sa.Column('linkedin', sa.String(400)))

def downgrade():
    op.drop_column('business', 'linkedin')
