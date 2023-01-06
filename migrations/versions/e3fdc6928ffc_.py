"""empty message

Revision ID: e3fdc6928ffc
Revises: 
Create Date: 2022-12-17 18:49:55.759430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3fdc6928ffc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    op.drop_table('book')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=True),
    sa.Column('author', sa.VARCHAR(length=120), nullable=True),
    sa.Column('category', sa.VARCHAR(length=120), nullable=True),
    sa.Column('description', sa.VARCHAR(length=120), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
