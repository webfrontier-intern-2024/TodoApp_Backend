"""create todo table

Revision ID: f77364370b15
Revises: 
Create Date: 2024-10-17 07:46:26.822144

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = "f77364370b15"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "todolist",
        sa.Column("id", sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table("todolist")
