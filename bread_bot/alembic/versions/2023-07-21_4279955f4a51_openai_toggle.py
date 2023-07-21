"""Openai toggle

Revision ID: 4279955f4a51
Revises: 127d7635f19e
Create Date: 2023-07-21 17:32:24.587622

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "4279955f4a51"
down_revision = "127d7635f19e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("chats", sa.Column("is_openai_enabled", sa.Boolean(), nullable=True))
    op.execute("UPDATE chats SET is_openai_enabled = false")
    op.alter_column("chats", "is_openai_enabled", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("chats", "is_openai_enabled")
    # ### end Alembic commands ###
