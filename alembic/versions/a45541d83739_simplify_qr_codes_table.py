"""simplify qr codes table

Revision ID: YOUR_NEW_REVISION_ID
Revises: 24c07f7e8204
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "YOUR_NEW_REVISION_ID"

down_revision: Union[str, Sequence[str], None] = "24c07f7e8204"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Remove wedding details from QR table.
    # These details now come directly from the weddings table.

    op.drop_column(
        "qr_codes",
        "couple_name",
    )

    op.drop_column(
        "qr_codes",
        "registry_link",
    )

    op.drop_column(
        "qr_codes",
        "wedding_date",
    )

    op.drop_column(
        "qr_codes",
        "wedding_venue",
    )

    op.drop_column(
        "qr_codes",
        "description",
    )


def downgrade() -> None:

    op.add_column(
        "qr_codes",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "qr_codes",
        sa.Column(
            "wedding_venue",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "qr_codes",
        sa.Column(
            "wedding_date",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "qr_codes",
        sa.Column(
            "registry_link",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "qr_codes",
        sa.Column(
            "couple_name",
            sa.String(length=150),
            nullable=True,
        ),
    )