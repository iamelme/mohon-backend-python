"""create users table

Revision ID: 242164d909b1
Revises: 76bd92b661a7
Create Date: 2023-05-27 01:01:45.706254

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = "242164d909b1"
down_revision = "76bd92b661a7"
branch_labels = None
depends_on = None

# first_name = Column(String, nullable=False)
# last_name = Column(String, nullable=False)
# email = Column(String, unique=True, index=True)
# password = Column(String, nullable=False)
# is_active = Column(Boolean, nullable=False, server_default="TRUE")
# role = Column(String, default="user")
# created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
# updated_at = Column(TIMESTAMP(timezone=True), onupdate=text("now()"))


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "user_id",
            sa.UUID(),
            nullable=False,
            primary_key=True,
            index=True,
            server_default=text("uuid_generate_v4()"),
        ),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), index=True, unique=True, nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), default="user"),
        sa.Column("is_active", sa.Boolean(), server_default="TRUE"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), onupdate=text("now()")),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
