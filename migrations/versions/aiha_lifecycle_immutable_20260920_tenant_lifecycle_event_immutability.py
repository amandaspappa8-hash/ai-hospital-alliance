"""Enforce append-only tenant lifecycle event history.

Revision ID: aiha_lifecycle_immut_20260920
Revises: aiha_tenant_lifecycle_20260919
Create Date: 2026-09-20

SEC-S6A P17C.

This migration adds database-level immutability enforcement for
tenant_data_lifecycle_events.

Allowed:
- SELECT
- INSERT

Rejected:
- UPDATE
- DELETE
- TRUNCATE

This migration does not introduce tenant purge authority, lifecycle
execution authority, destructive HTTP endpoints, or event deletion.
"""

from typing import Optional, Sequence, Union

from alembic import op


revision: str = "aiha_lifecycle_immut_20260920"
down_revision: Union[str, Sequence[str], None] = (
    "aiha_tenant_lifecycle_20260919"
)
branch_labels: Optional[Union[str, Sequence[str]]] = None
depends_on: Optional[Union[str, Sequence[str]]] = None


IMMUTABILITY_FUNCTION = """
CREATE FUNCTION public.aiha_prevent_tenant_lifecycle_event_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $aiha_lifecycle_immutability$
BEGIN
    RAISE EXCEPTION
        USING
            ERRCODE = '55000',
            MESSAGE = format(
                'tenant_data_lifecycle_events is append-only; %s is forbidden',
                TG_OP
            );
    RETURN NULL;
END;
$aiha_lifecycle_immutability$;
"""


ROW_IMMUTABILITY_TRIGGER = """
CREATE TRIGGER trg_aiha_tenant_lifecycle_events_immutable_rows
BEFORE UPDATE OR DELETE
ON public.tenant_data_lifecycle_events
FOR EACH ROW
EXECUTE FUNCTION public.aiha_prevent_tenant_lifecycle_event_mutation();
"""


TRUNCATE_IMMUTABILITY_TRIGGER = """
CREATE TRIGGER trg_aiha_tenant_lifecycle_events_immutable_truncate
BEFORE TRUNCATE
ON public.tenant_data_lifecycle_events
FOR EACH STATEMENT
EXECUTE FUNCTION public.aiha_prevent_tenant_lifecycle_event_mutation();
"""


def upgrade() -> None:
    """Install database-level append-only protection."""
    op.execute(IMMUTABILITY_FUNCTION)
    op.execute(ROW_IMMUTABILITY_TRIGGER)
    op.execute(TRUNCATE_IMMUTABILITY_TRIGGER)


def downgrade() -> None:
    """Remove protection objects without deleting lifecycle event data."""
    op.execute(
        """
        DROP TRIGGER IF EXISTS
        trg_aiha_tenant_lifecycle_events_immutable_truncate
        ON public.tenant_data_lifecycle_events;
        """
    )
    op.execute(
        """
        DROP TRIGGER IF EXISTS
        trg_aiha_tenant_lifecycle_events_immutable_rows
        ON public.tenant_data_lifecycle_events;
        """
    )
    op.execute(
        """
        DROP FUNCTION IF EXISTS
        public.aiha_prevent_tenant_lifecycle_event_mutation();
        """
    )
