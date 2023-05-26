"""create posts table

Revision ID: 50294994d0b5
Revises: 
Create Date: 2023-05-27 00:19:31.429105

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = "50294994d0b5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("post_id", sa.UUID(), nullable=False, primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("is_publish", sa.Boolean(), nullable=False, server_default="FALSE"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=True, onupdate=text("now()")),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
