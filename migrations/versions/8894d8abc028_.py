"""empty message

Revision ID: 8894d8abc028
Revises: 2308704d9d94
Create Date: 2021-03-03 02:55:47.779437

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8894d8abc028'
down_revision = '2308704d9d94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Planeta', sa.Column('creacion', sa.String(length=250), nullable=True))
    op.add_column('Planeta', sa.Column('editado', sa.String(length=250), nullable=True))
    op.drop_column('Planeta', 'residentes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Planeta', sa.Column('residentes', mysql.VARCHAR(length=250), nullable=True))
    op.drop_column('Planeta', 'editado')
    op.drop_column('Planeta', 'creacion')
    # ### end Alembic commands ###
