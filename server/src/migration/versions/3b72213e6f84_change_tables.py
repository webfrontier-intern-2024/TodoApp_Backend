"""change tables

Revision ID: 3b72213e6f84
Revises: 67d25f1f1c5b
Create Date: 2024-10-29 10:14:09.135056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b72213e6f84'
down_revision: Union[str, None] = '67d25f1f1c5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('tags', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_tags_created_at'), 'tags', ['created_at'], unique=False)
    op.create_index(op.f('ix_tags_updated_at'), 'tags', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tags_updated_at'), table_name='tags')
    op.drop_index(op.f('ix_tags_created_at'), table_name='tags')
    op.drop_column('tags', 'updated_at')
    op.drop_column('tags', 'created_at')
    # ### end Alembic commands ###