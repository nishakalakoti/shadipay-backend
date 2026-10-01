"""simplify qr codes table

Revision ID: 36360a4edb74
Revises: YOUR_NEW_REVISION_ID
Create Date: 2026-09-30 12:22:14.090697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '36360a4edb74'
down_revision: Union[str, Sequence[str], None] = 'YOUR_NEW_REVISION_ID'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
