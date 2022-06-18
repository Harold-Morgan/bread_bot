"""add data_voice

Revision ID: 379fd0a9186b
Revises: 8f91b5211c28
Create Date: 2022-06-18 05:19:12.057631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '379fd0a9186b'
down_revision = '8f91b5211c28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('local_memes', sa.Column('data_voice', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('local_memes', 'data_voice')
    # ### end Alembic commands ###
