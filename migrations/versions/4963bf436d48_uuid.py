"""uuid

Revision ID: 4963bf436d48
Revises: e3fdc6928ffc
Create Date: 2022-12-19 20:07:20.279392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4963bf436d48'
down_revision = 'e3fdc6928ffc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=200),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
