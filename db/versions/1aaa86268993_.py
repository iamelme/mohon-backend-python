""" change column name from post_id to id and user_id to id

Revision ID: 1aaa86268993
Revises: 242164d909b1
Create Date: 2023-05-27 01:25:03.362388

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1aaa86268993"
down_revision = "242164d909b1"
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
