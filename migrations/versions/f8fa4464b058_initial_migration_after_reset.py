"""Initial migration after reset

Revision ID: f8fa4464b058
Revises: 
Create Date: 2024-07-24 14:38:37.262637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8fa4464b058'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cooking_time', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('difficulty_level', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('recipe_type', sa.String(), nullable=False))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shopping_list', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('shopping_list')

    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.drop_column('recipe_type')
        batch_op.drop_column('difficulty_level')
        batch_op.drop_column('cooking_time')

    # ### end Alembic commands ###
