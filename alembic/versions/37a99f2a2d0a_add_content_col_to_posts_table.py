"""add content col to posts table

Revision ID: 37a99f2a2d0a
Revises: fa588e59460f
Create Date: 2022-01-07 14:13:10.349184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37a99f2a2d0a'
down_revision = 'fa588e59460f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
