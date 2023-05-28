"""update default value of user field is_active to false

Revision ID: 5ae8ff50ccb8
Revises: eb406645a053
Create Date: 2023-05-28 12:34:20.967284

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5ae8ff50ccb8"
down_revision = "eb406645a053"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "posts",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column("posts", "user_id", existing_type=sa.UUID(), nullable=False)
    op.create_index(op.f("ix_posts_id"), "posts", ["id"], unique=True)
    op.drop_constraint("post_user_fk", "posts", type_="foreignkey")
    op.create_foreign_key(None, "posts", "users", ["user_id"], ["id"], ondelete="CASCADE")
    op.alter_column("users", "email", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("users", "is_active", existing_type=sa.BOOLEAN(), nullable=False, server_default=sa.text("false"))
    op.drop_index("ix_users_user_id", table_name="users")
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.create_index("ix_users_user_id", "users", ["id"], unique=False)
    op.alter_column(
        "users", "is_active", existing_type=sa.BOOLEAN(), nullable=True, existing_server_default=sa.text("true")
    )
    op.alter_column("users", "email", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_constraint(None, "posts", type_="foreignkey")
    op.create_foreign_key("post_user_fk", "posts", "users", ["user_id"], ["id"])
    op.drop_index(op.f("ix_posts_id"), table_name="posts")
    op.alter_column("posts", "user_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        "posts",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    # ### end Alembic commands ###