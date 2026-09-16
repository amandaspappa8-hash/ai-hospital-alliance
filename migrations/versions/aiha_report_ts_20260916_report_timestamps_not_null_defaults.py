"""Report timestamps NOT NULL and UTC-naive server defaults.

Revision ID: aiha_report_ts_20260916
Revises: aiha_report_mac_20260916
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision: str = "aiha_report_ts_20260916"
down_revision: str | None = "aiha_report_mac_20260916"
branch_labels = None
depends_on = None


_UTC_NAIVE_NOW = sa.text(
    "(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"
)


def upgrade() -> None:
    """Harden canonical Reports timestamp persistence."""

    # Backfill remains required even when the table is currently empty.
    # It makes the migration safe if rows are created before deployment.
    op.execute(
        """
        UPDATE public.reports
        SET created_at =
            (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        WHERE created_at IS NULL
        """
    )

    op.execute(
        """
        UPDATE public.reports
        SET updated_at =
            COALESCE(
                created_at,
                CURRENT_TIMESTAMP AT TIME ZONE 'UTC'
            )
        WHERE updated_at IS NULL
        """
    )

    op.alter_column(
        "reports",
        "created_at",
        schema="public",
        existing_type=sa.DateTime(
            timezone=False
        ),
        nullable=False,
        server_default=_UTC_NAIVE_NOW,
    )

    op.alter_column(
        "reports",
        "updated_at",
        schema="public",
        existing_type=sa.DateTime(
            timezone=False
        ),
        nullable=False,
        server_default=_UTC_NAIVE_NOW,
    )


def downgrade() -> None:
    """Restore the prior nullable/no-default timestamp schema."""

    op.alter_column(
        "reports",
        "updated_at",
        schema="public",
        existing_type=sa.DateTime(
            timezone=False
        ),
        nullable=True,
        server_default=None,
    )

    op.alter_column(
        "reports",
        "created_at",
        schema="public",
        existing_type=sa.DateTime(
            timezone=False
        ),
        nullable=True,
        server_default=None,
    )
