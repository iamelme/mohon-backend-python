"""add column tags to table posts

Revision ID: 76bd92b661a7
Revises: 50294994d0b5
Create Date: 2023-05-27 00:55:15.558033

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "76bd92b661a7"
down_revision = "50294994d0b5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("tags", sa.ARRAY(sa.String()), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("posts", "tags")
    pass
