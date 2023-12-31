"""Create user table

Revision ID: 7a91fe899024
Revises: ff318a784072
Create Date: 2023-12-09 17:27:55.833717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a91fe899024"
down_revision = "ff318a784072"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_user_username"), ["username"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_user_username"))

    op.drop_table("user")
    # ### end Alembic commands ###
