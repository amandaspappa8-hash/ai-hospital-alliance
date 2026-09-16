"""Add explicit key identity to report content MAC baselines.

Revision ID: aiha_report_mac_keyid_20260916
Revises: aiha_report_ts_20260916
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision: str = "aiha_report_mac_keyid_20260916"
down_revision: str | None = "aiha_report_ts_20260916"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add non-secret MAC key identity with zero-row fail-safe."""

    connection = op.get_bind()

    existing_rows = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM public.report_content_macs
            """
        )
    ).scalar_one()

    if int(existing_rows) != 0:
        raise RuntimeError(
            "AIHA report MAC key_id migration requires "
            "public.report_content_macs to contain zero rows"
        )

    op.add_column(
        "report_content_macs",
        sa.Column(
            "key_id",
            sa.String(length=64),
            nullable=False,
        ),
        schema="public",
    )


def downgrade() -> None:
    """Remove only the key identity metadata column."""

    op.drop_column(
        "report_content_macs",
        "key_id",
        schema="public",
    )
