"""increasing business description field to 2K characters

Revision ID: 3b9b1a8230ba
Revises: 2982c567e452
Create Date: 2014-10-12 09:38:52.458179

"""

# revision identifiers, used by Alembic.
revision = '3b9b1a8230ba'
down_revision = '2982c567e452'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('business', 'description', type_=sa.String(2000))

def downgrade():
    op.alter_column('business', 'description', type_=sa.String(1200))
