"""empty message

Revision ID: 6b9989be4376
Revises: c42dd8acf471
Create Date: 2018-12-22 19:35:33.112000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6b9989be4376'
down_revision = 'c42dd8acf471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('record_income_expenditure', 'creator',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=64),
               nullable=False)
    op.alter_column('record_income_expenditure', 'creator_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('record_income_expenditure', 'ctime',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('record_income_expenditure', 'entry_account_status',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('record_income_expenditure', 'entry_account_time',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('record_income_expenditure', 'record_content',
               existing_type=mysql.TEXT(collation=u'utf8_unicode_ci'),
               nullable=False)
    op.alter_column('record_income_expenditure', 'remark',
               existing_type=mysql.TEXT(collation=u'utf8_unicode_ci'),
               nullable=False)
    op.alter_column('record_income_expenditure', 'reviewer',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=64),
               nullable=False)
    op.alter_column('record_income_expenditure', 'reviewer_id',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=64),
               nullable=False)
    op.alter_column('record_income_expenditure', 'utime',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.drop_index('ix_record_income_expenditure_creator', table_name='record_income_expenditure')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_record_income_expenditure_creator', 'record_income_expenditure', ['creator'], unique=False)
    op.alter_column('record_income_expenditure', 'utime',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('record_income_expenditure', 'reviewer_id',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=64),
               nullable=True)
    op.alter_column('record_income_expenditure', 'reviewer',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=64),
               nullable=True)
    op.alter_column('record_income_expenditure', 'remark',
               existing_type=mysql.TEXT(collation=u'utf8_unicode_ci'),
               nullable=True)
    op.alter_column('record_income_expenditure', 'record_content',
               existing_type=mysql.TEXT(collation=u'utf8_unicode_ci'),
               nullable=True)
    op.alter_column('record_income_expenditure', 'entry_account_time',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('record_income_expenditure', 'entry_account_status',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('record_income_expenditure', 'ctime',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('record_income_expenditure', 'creator_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('record_income_expenditure', 'creator',
               existing_type=mysql.VARCHAR(collation=u'utf8_unicode_ci', length=64),
               nullable=True)
    # ### end Alembic commands ###