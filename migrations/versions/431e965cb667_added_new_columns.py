"""Added new columns

Revision ID: 431e965cb667
Revises: d3d73c49bd50
Create Date: 2024-07-26 17:02:28.866238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '431e965cb667'
down_revision = 'd3d73c49bd50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('new_usename', sa.String(length=150), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('new_usename')

    # ### end Alembic commands ###