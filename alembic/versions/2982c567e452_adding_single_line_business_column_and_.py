"""adding single line business column and removing the projection column

Revision ID: 2982c567e452
Revises: 144ab2a91bad
Create Date: 2014-10-08 11:51:46.655039

"""

# revision identifiers, used by Alembic.
revision = '2982c567e452'
down_revision = '144ab2a91bad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('business', sa.Column('raw_address', sa.String(300)))
    op.drop_column('business', 'projection')
    op.drop_column('event', 'projection')

def downgrade():
    op.drop_column('business', 'raw_address')
    op.add_column('event', sa.Column('projection', sa.String(15)))
    op.add_column('business', sa.Column('projection', sa.String(15)))
