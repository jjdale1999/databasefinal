"""empty message

Revision ID: cfa57e920db7
Revises: 
Create Date: 2020-03-10 17:09:20.772068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfa57e920db7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.String(length=80), nullable=True),
    sa.Column('lname', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('location', sa.String(length=80), nullable=True),
    sa.Column('gender', sa.String(length=80), nullable=True),
    sa.Column('biography', sa.Text(), nullable=True),
    sa.Column('photo', sa.String(length=80), nullable=True),
    sa.Column('created_date', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profiles')
    # ### end Alembic commands ###
