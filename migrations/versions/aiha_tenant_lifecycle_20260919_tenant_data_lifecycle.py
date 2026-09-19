"""Create canonical tenant data lifecycle authority.

SEC-S6A P14F

Revision ID: aiha_tenant_lifecycle_20260919
Revises: aiha_report_mac_keyid_20260916
Create Date: 2026-09-19

This migration creates persistence for tenant data-governance lifecycle
state and append-only lifecycle event history.

It intentionally does not:
- infer lifecycle state from tenants.is_active or tenants.is_verified
- backfill existing tenants
- implement hard deletion or purge
- implement automatic deletion
- add tenant DELETE or export HTTP endpoints
- alter public.tenants or public.users
- delete clinical data

Destructive operations must remain fail-closed when no lifecycle
authority exists for a tenant.
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "aiha_tenant_lifecycle_20260919"
down_revision: str | None = "aiha_report_mac_keyid_20260916"
branch_labels = None
depends_on = None


_LIFECYCLE_STATE_CHECK = (
    "lifecycle_state IN ("
    "'ACTIVE',"
    "'SUSPENDED',"
    "'OFFBOARDING_REQUESTED',"
    "'RETENTION_HOLD',"
    "'ARCHIVED',"
    "'PURGE_PENDING'"
    ")"
)


def upgrade() -> None:
    """Create tenant lifecycle state and event persistence."""

    op.create_table(
        "tenant_data_lifecycle",
        sa.Column(
            "tenant_id",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "lifecycle_state",
            sa.String(length=40),
            nullable=False,
        ),
        sa.Column(
            "legal_hold_active",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "legal_hold_reason",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "legal_hold_set_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "legal_hold_released_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "retention_until",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "offboarding_requested_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "offboarding_approved_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "archive_completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "purge_eligible_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            _LIFECYCLE_STATE_CHECK,
            name="ck_tenant_data_lifecycle_state",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["public.tenants.id"],
            name="fk_tenant_data_lifecycle_tenant_id",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "tenant_id",
            name="pk_tenant_data_lifecycle",
        ),
        schema="public",
    )

    op.create_table(
        "tenant_data_lifecycle_events",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "event_type",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "actor_user_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "reason",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "metadata",
            postgresql.JSONB(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["public.tenants.id"],
            name="fk_tenant_data_lifecycle_events_tenant_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["actor_user_id"],
            ["public.users.id"],
            name="fk_tenant_data_lifecycle_events_actor_user_id",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_tenant_data_lifecycle_events",
        ),
        schema="public",
    )

    op.create_index(
        "ix_tenant_data_lifecycle_events_tenant_occurred",
        "tenant_data_lifecycle_events",
        ["tenant_id", "occurred_at"],
        unique=False,
        schema="public",
    )


def downgrade() -> None:
    """Remove only lifecycle persistence introduced by this migration."""

    op.drop_index(
        "ix_tenant_data_lifecycle_events_tenant_occurred",
        table_name="tenant_data_lifecycle_events",
        schema="public",
    )

    op.drop_table(
        "tenant_data_lifecycle_events",
        schema="public",
    )

    op.drop_table(
        "tenant_data_lifecycle",
        schema="public",
    )
