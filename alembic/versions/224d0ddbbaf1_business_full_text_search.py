"""Business full-text search

Revision ID: 224d0ddbbaf1
Revises: 47117eed1c58
Create Date: 2014-10-19 19:06:51.890618

"""

# revision identifiers, used by Alembic.
revision = '224d0ddbbaf1'
down_revision = '47117eed1c58'

from alembic import op
import sqlalchemy as sa
from sqlalchemy_searchable import sync_trigger
from sqlalchemy_utils.types import TSVectorType

def upgrade():
    op.add_column('business', sa.Column('search_vector', TSVectorType('name', 'category', 'description')))
    
    conn = op.get_bind()
    sync_trigger(conn, 'business', 'search_vector', ['name', 'category', 'description'])

def downgrade():
    op.drop_column('business', 'search_vector')
    conn = op.get_bind()
    sync_trigger(conn, 'business', 'search_vector', ['name', 'category', 'description'])