"""change default value for is_field from true to false from table users

Revision ID: 94fb1500b531
Revises: 5ae8ff50ccb8
Create Date: 2023-05-28 12:49:14.166613

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "94fb1500b531"
down_revision = "5ae8ff50ccb8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users", column_name="is_active", server_default="false")
    pass


def downgrade() -> None:
    op.alter_column("users", column_name="is_active", server_default="true")
    pass
