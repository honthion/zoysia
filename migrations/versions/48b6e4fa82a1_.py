"""empty message

Revision ID: 48b6e4fa82a1
Revises: 
Create Date: 2018-12-22 08:27:24.727000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '48b6e4fa82a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sys_user', sa.Column('ctime', sa.DateTime(), nullable=True))
    op.add_column('sys_user', sa.Column('utime', sa.DateTime(), nullable=True))
    op.drop_column('sys_user', 'pub_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sys_user', sa.Column('pub_date', mysql.DATETIME(), nullable=True))
    op.drop_column('sys_user', 'utime')
    op.drop_column('sys_user', 'ctime')
    # ### end Alembic commands ###
