"""add relationships to tables posts and users

Revision ID: eb406645a053
Revises: 9e9fb67b8bec
Create Date: 2023-05-27 02:24:50.713348

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eb406645a053"
down_revision = "9e9fb67b8bec"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.UUID()))
    op.create_foreign_key(
        constraint_name="post_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
