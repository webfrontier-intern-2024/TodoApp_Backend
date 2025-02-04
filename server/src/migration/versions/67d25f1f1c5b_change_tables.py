"""change tables

Revision ID: 67d25f1f1c5b
Revises: 
Create Date: 2024-10-29 10:12:36.276751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67d25f1f1c5b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('tagID', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('tagName', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('tagID')
    )
    op.create_index(op.f('ix_tags_tagID'), 'tags', ['tagID'], unique=False)
    op.create_index(op.f('ix_tags_tagName'), 'tags', ['tagName'], unique=False)
    op.create_table('todoLists',
    sa.Column('todoID', sa.UUID(), nullable=False),
    sa.Column('taskName', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('finished', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('tagID', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['tagID'], ['tags.tagID'], ),
    sa.PrimaryKeyConstraint('todoID')
    )
    op.create_index(op.f('ix_todoLists_created_at'), 'todoLists', ['created_at'], unique=False)
    op.create_index(op.f('ix_todoLists_description'), 'todoLists', ['description'], unique=False)
    op.create_index(op.f('ix_todoLists_finished'), 'todoLists', ['finished'], unique=False)
    op.create_index(op.f('ix_todoLists_tagID'), 'todoLists', ['tagID'], unique=False)
    op.create_index(op.f('ix_todoLists_taskName'), 'todoLists', ['taskName'], unique=False)
    op.create_index(op.f('ix_todoLists_todoID'), 'todoLists', ['todoID'], unique=False)
    op.create_index(op.f('ix_todoLists_updated_at'), 'todoLists', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_todoLists_updated_at'), table_name='todoLists')
    op.drop_index(op.f('ix_todoLists_todoID'), table_name='todoLists')
    op.drop_index(op.f('ix_todoLists_taskName'), table_name='todoLists')
    op.drop_index(op.f('ix_todoLists_tagID'), table_name='todoLists')
    op.drop_index(op.f('ix_todoLists_finished'), table_name='todoLists')
    op.drop_index(op.f('ix_todoLists_description'), table_name='todoLists')
    op.drop_index(op.f('ix_todoLists_created_at'), table_name='todoLists')
    op.drop_table('todoLists')
    op.drop_index(op.f('ix_tags_tagName'), table_name='tags')
    op.drop_index(op.f('ix_tags_tagID'), table_name='tags')
    op.drop_table('tags')
    # ### end Alembic commands ###
