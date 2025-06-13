"""init

Revision ID: 37c6fa73b7eb
Revises: 
Create Date: 2025-03-23 18:02:14.472378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37c6fa73b7eb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tracks',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=True),
    sa.Column('artist', sa.String(length=60), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('cover_path', sa.Text(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('tracks')
    # ### end Alembic commands ###
