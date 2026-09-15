"""Add canonical summary storage to public.reports.

Revision ID: aiha_reports_summary_20260915
Revises: aiha_oph_schema_20260913

This migration preserves the existing Reports API summary field in
canonical PostgreSQL storage.

No data backfill is required because public.reports contained zero rows
at the migration design preflight.
"""

from alembic import op
import sqlalchemy as sa


revision = "aiha_reports_summary_20260915"
down_revision = "aiha_oph_schema_20260913"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add nullable summary storage to canonical Reports."""

    op.add_column(
        "reports",
        sa.Column(
            "summary",
            sa.Text(),
            nullable=True,
        ),
        schema="public",
    )


def downgrade() -> None:
    """Remove canonical Reports summary storage."""

    op.drop_column(
        "reports",
        "summary",
        schema="public",
    )
