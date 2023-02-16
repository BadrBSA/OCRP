"""add content column to posts table

Revision ID: 64e8f70d973e
Revises: 3d1d3ba58ca6
Create Date: 2023-02-16 11:26:27.885710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64e8f70d973e'
down_revision = '3d1d3ba58ca6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
