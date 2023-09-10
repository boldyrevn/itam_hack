"""added captain_id field

Revision ID: 9a87437382f5
Revises: 82f50165ec86
Create Date: 2023-09-10 19:07:23.444089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a87437382f5'
down_revision: Union[str, None] = '82f50165ec86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('captain_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'captain_id')
    # ### end Alembic commands ###