"""AIHA Phase 2.7: canonical patient tenant-scope foundation.

Creates the explicit auth-to-canonical tenant identity bridge and adds a
nullable canonical tenant ownership reference to hospitals.

Schema only:
- no tenant identity mappings
- no hospital ownership backfill
- no patient data changes
- no NOT NULL enforcement
- no patient read/write cutover
"""

from alembic import op


revision = "aiha_pat_tenant_scope_20260906"
down_revision = "aiha_live_20260903"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Auth tenant UUID -> canonical tenant string ID.
    #
    # auth_tenant_id is the primary key, enforcing one bridge row per
    # authenticated tenant. canonical_tenant_id is UNIQUE, enforcing the
    # reviewed one-to-one mapping policy.
    op.execute(
        """
        CREATE TABLE public.tenant_identity_bridge (
            auth_tenant_id UUID NOT NULL,
            canonical_tenant_id VARCHAR NOT NULL,
            CONSTRAINT tenant_identity_bridge_pkey
                PRIMARY KEY (auth_tenant_id),
            CONSTRAINT tenant_identity_bridge_canonical_tenant_id_key
                UNIQUE (canonical_tenant_id),
            CONSTRAINT tenant_identity_bridge_canonical_tenant_id_fkey
                FOREIGN KEY (canonical_tenant_id)
                REFERENCES public.tenants(id)
        )
        """
    )

    # Canonical hospital ownership is intentionally nullable at this stage.
    # Ownership values require a separately reviewed explicit mapping.
    op.execute(
        """
        ALTER TABLE public.hospitals
        ADD COLUMN tenant_id VARCHAR NULL
        """
    )

    op.execute(
        """
        ALTER TABLE public.hospitals
        ADD CONSTRAINT hospitals_tenant_id_fkey
        FOREIGN KEY (tenant_id)
        REFERENCES public.tenants(id)
        """
    )

    op.execute(
        """
        CREATE INDEX ix_hospitals_tenant_id
        ON public.hospitals (tenant_id)
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS public.ix_hospitals_tenant_id
        """
    )

    op.execute(
        """
        ALTER TABLE public.hospitals
        DROP CONSTRAINT IF EXISTS hospitals_tenant_id_fkey
        """
    )

    op.execute(
        """
        ALTER TABLE public.hospitals
        DROP COLUMN IF EXISTS tenant_id
        """
    )

    op.execute(
        """
        DROP TABLE IF EXISTS public.tenant_identity_bridge
        """
    )
