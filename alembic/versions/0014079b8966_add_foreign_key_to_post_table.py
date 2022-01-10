"""add foreign key to post table

Revision ID: 0014079b8966
Revises: 7ce42dc5a8da
Create Date: 2022-01-10 10:17:16.989198

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null, table


# revision identifiers, used by Alembic.
revision = '0014079b8966'
down_revision = '7ce42dc5a8da'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', 
                            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass