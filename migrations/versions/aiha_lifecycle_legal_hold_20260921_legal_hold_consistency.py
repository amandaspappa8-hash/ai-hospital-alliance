"""Enforce tenant legal-hold field consistency.

SEC-S6A P19D

Revision ID: aiha_lifecycle_lh_20260921
Revises: aiha_lifecycle_uat_20260921
Create Date: 2026-09-21

This migration adds an internal legal-hold consistency invariant to
public.tenant_data_lifecycle.

It intentionally does not:
- couple legal_hold_active to lifecycle_state='RETENTION_HOLD';
- couple legal_hold_active to retention_until;
- alter lifecycle-state values;
- mutate lifecycle rows;
- mutate lifecycle events;
- backfill data.
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op


revision: str = "aiha_lifecycle_lh_20260921"
down_revision: Union[str, Sequence[str], None] = (
    "aiha_lifecycle_uat_20260921"
)
branch_labels = None
depends_on = None


_CONSTRAINT_NAME = (
    "ck_tenant_data_lifecycle_legal_hold_consistency"
)

_CONSTRAINT_SQL = """
(
    (
        legal_hold_active = TRUE
        AND legal_hold_reason IS NOT NULL
        AND btrim(legal_hold_reason) <> ''
        AND legal_hold_set_at IS NOT NULL
        AND legal_hold_released_at IS NULL
    )
    OR
    (
        legal_hold_active = FALSE
        AND (
            legal_hold_released_at IS NULL
            OR legal_hold_set_at IS NOT NULL
        )
    )
)
"""


def upgrade() -> None:
    """Add legal-hold internal consistency check."""

    op.create_check_constraint(
        _CONSTRAINT_NAME,
        "tenant_data_lifecycle",
        _CONSTRAINT_SQL,
        schema="public",
    )


def downgrade() -> None:
    """Remove only the legal-hold consistency check."""

    op.drop_constraint(
        _CONSTRAINT_NAME,
        "tenant_data_lifecycle",
        schema="public",
        type_="check",
    )
