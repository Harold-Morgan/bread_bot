"""AnswerEntity migration

Revision ID: 3e65a3ee9c7e
Revises: a447984ded8d
Create Date: 2022-10-28 22:06:33.235829

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3e65a3ee9c7e"
down_revision = "a447984ded8d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "gif_entities",
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("reaction_type", sa.Enum("TRIGGER", "SUBSTRING", name="answerentitytypesenum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "photo_entities",
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("reaction_type", sa.Enum("TRIGGER", "SUBSTRING", name="answerentitytypesenum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sticker_entities",
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("reaction_type", sa.Enum("TRIGGER", "SUBSTRING", name="answerentitytypesenum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "text_entities",
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("reaction_type", sa.Enum("TRIGGER", "SUBSTRING", name="answerentitytypesenum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "voice_entities",
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("reaction_type", sa.Enum("TRIGGER", "SUBSTRING", name="answerentitytypesenum"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("voice_entities")
    op.drop_table("text_entities")
    op.drop_table("sticker_entities")
    op.drop_table("photo_entities")
    op.drop_table("gif_entities")
    # ### end Alembic commands ###
