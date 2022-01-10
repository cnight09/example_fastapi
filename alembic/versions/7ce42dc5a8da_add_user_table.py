"""add user table

Revision ID: 7ce42dc5a8da
Revises: 37a99f2a2d0a
Create Date: 2022-01-10 10:03:50.646478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '7ce42dc5a8da'
down_revision = '37a99f2a2d0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                             sa.Column('email', sa.String(), nullable=False),
                             sa.Column('password', sa.String(), nullable=False),
                             sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                        server_default=sa.text('now()'), nullable=False),
                             sa.PrimaryKeyConstraint('id'),
                             sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
