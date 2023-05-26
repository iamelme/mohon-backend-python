"""rename column post_id to id and user_id to id

Revision ID: 9e9fb67b8bec
Revises: 1aaa86268993
Create Date: 2023-05-27 02:12:26.034884

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9e9fb67b8bec"
down_revision = "1aaa86268993"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("posts", column_name="post_id", new_column_name="id", existing_type=sa.UUID())
    op.alter_column("users", column_name="user_id", new_column_name="id")
    pass


def downgrade() -> None:
    op.alter_column("posts", column_name="id", new_column_name="post_id")
    op.alter_column("users", column_name="id", new_column_name="user_id")
    pass
