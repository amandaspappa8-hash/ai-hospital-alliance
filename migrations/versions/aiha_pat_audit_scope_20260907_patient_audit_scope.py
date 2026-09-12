"""Add canonical tenant scope to public.audit_logs.

This migration is intentionally additive and minimal.

It adds one nullable VARCHAR tenant_id column to public.audit_logs so
canonical Patient PostgreSQL writes can record the real tenant identifier
without coercing integer user identifiers or VARCHAR tenant identifiers
into the legacy UUID audit domain.

No historical audit rows are backfilled because their tenant provenance is
not established by the canonical authority chain.

Revision ID: aiha_pat_audit_scope_20260907
Revises: aiha_pat_api_enrich_20260907
"""

from alembic import op
import sqlalchemy as sa


revision = "aiha_pat_audit_scope_20260907"
down_revision = "aiha_pat_api_enrich_20260907"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "audit_logs",
        sa.Column(
            "tenant_id",
            sa.String(),
            nullable=True,
        ),
        schema="public",
    )


def downgrade() -> None:
    op.drop_column(
        "audit_logs",
        "tenant_id",
        schema="public",
    )
