"""add default column on Role

Revision ID: 795964fd3aa5
Revises: d8d27f7a7921
Create Date: 2022-02-23 16:06:52.499634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '795964fd3aa5'
down_revision = 'd8d27f7a7921'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###
