"""create qr codes table

Revision ID: 24c07f7e8204
Revises: a6e4cf6f0c2d
Create Date: 2026-09-30 11:14:13.462823
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "24c07f7e8204"

down_revision: Union[str, Sequence[str], None] = "a6e4cf6f0c2d"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "qr_codes",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "wedding_id",
            sa.Integer(),
            sa.ForeignKey(
                "weddings.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "couple_name",
            sa.String(length=150),
            nullable=False,
        ),

        sa.Column(
            "registry_link",
            sa.String(length=500),
            nullable=False,
        ),

        sa.Column(
            "wedding_date",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "wedding_venue",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "qr_image_url",
            sa.String(length=500),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "wedding_id",
            name="uq_qr_codes_wedding_id",
        ),
    )

    op.create_index(
        "ix_qr_codes_id",
        "qr_codes",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_qr_codes_wedding_id",
        "qr_codes",
        ["wedding_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_qr_codes_wedding_id",
        table_name="qr_codes",
    )

    op.drop_index(
        "ix_qr_codes_id",
        table_name="qr_codes",
    )

    op.drop_table("qr_codes")