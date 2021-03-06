"""empty message

Revision ID: 2308704d9d94
Revises: 519ee25ab402
Create Date: 2021-03-03 02:16:00.650338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2308704d9d94'
down_revision = '519ee25ab402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Personajes', sa.Column('altura', sa.String(length=250), nullable=True))
    op.drop_column('Personajes', 'terreno')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Personajes', sa.Column('terreno', mysql.VARCHAR(length=250), nullable=True))
    op.drop_column('Personajes', 'altura')
    # ### end Alembic commands ###
