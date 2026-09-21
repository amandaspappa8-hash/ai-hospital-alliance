"""Reject blank or whitespace-only tenant lifecycle event types.

SEC-S6A P20D.

Revision ID: aiha_lifecycle_evtfmt_20260921
Revises: aiha_lifecycle_lh_20260921
Create Date: 2026-09-21

This migration adds a format-only CHECK constraint to
public.tenant_data_lifecycle_events.event_type.

It intentionally does not:
- enumerate allowed event types;
- define an event vocabulary;
- restrict future event names;
- impose case or prefix conventions;
- introduce a lifecycle event writer;
- mutate lifecycle event data.

The existing VARCHAR(64) and NOT NULL constraints remain authoritative for
length and nullability. This control only rejects empty or whitespace-only
event_type values.
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op


revision: str = "aiha_lifecycle_evtfmt_20260921"
down_revision: Union[str, Sequence[str], None] = (
    "aiha_lifecycle_lh_20260921"
)
branch_labels = None
depends_on = None


_CONSTRAINT_NAME = (
    "ck_tenant_data_lifecycle_events_event_type_nonblank"
)

_CONSTRAINT_SQL = (
    "event_type !~ '^[[:space:]]*$'"
)


def upgrade() -> None:
    """Reject empty or whitespace-only lifecycle event types."""

    op.create_check_constraint(
        _CONSTRAINT_NAME,
        "tenant_data_lifecycle_events",
        _CONSTRAINT_SQL,
        schema="public",
    )


def downgrade() -> None:
    """Remove only the lifecycle event-type format check."""

    op.drop_constraint(
        _CONSTRAINT_NAME,
        "tenant_data_lifecycle_events",
        schema="public",
        type_="check",
    )
