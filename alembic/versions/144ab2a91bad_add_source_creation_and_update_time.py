"""add source creation and update time

Revision ID: 144ab2a91bad
Revises: None
Create Date: 2014-10-06 10:06:23.961087

"""

# revision identifiers, used by Alembic.
revision = '144ab2a91bad'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('source', sa.Column('created_on', sa.DateTime))
    op.add_column('source', sa.Column('updated_on', sa.DateTime))

def downgrade():
    op.drop_column('source', 'created_on')
    op.drop_column('source', 'updated_on')
