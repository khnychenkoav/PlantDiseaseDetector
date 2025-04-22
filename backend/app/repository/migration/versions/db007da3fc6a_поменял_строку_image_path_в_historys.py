"""Поменял строку image_path в historys

Revision ID: db007da3fc6a
Revises: d94e32c79b92
Create Date: 2025-04-22 19:50:46.783458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db007da3fc6a'
down_revision: Union[str, None] = 'd94e32c79b92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
