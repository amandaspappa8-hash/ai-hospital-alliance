"""Automate tenant lifecycle updated_at on row updates.

SEC-S6A P18C.

This migration adds database-level updated_at automation only for
public.tenant_data_lifecycle.

The append-only public.tenant_data_lifecycle_events table is intentionally
outside this migration and remains governed by the existing immutability
triggers.

No purge authority, destructive execution authority, legal-hold semantics,
event-type policy, RLS policy, or application API contract is introduced here.
"""

from typing import Sequence, Union

from alembic import op


revision: str = "aiha_lifecycle_updated_at_20260921"
down_revision: Union[str, Sequence[str], None] = (
    "aiha_lifecycle_immut_20260920"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE FUNCTION public.aiha_set_tenant_data_lifecycle_updated_at()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $function$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $function$
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_aiha_tenant_data_lifecycle_updated_at
        BEFORE UPDATE
        ON public.tenant_data_lifecycle
        FOR EACH ROW
        EXECUTE FUNCTION public.aiha_set_tenant_data_lifecycle_updated_at()
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER trg_aiha_tenant_data_lifecycle_updated_at
        ON public.tenant_data_lifecycle
        """
    )

    op.execute(
        """
        DROP FUNCTION public.aiha_set_tenant_data_lifecycle_updated_at()
        """
    )
