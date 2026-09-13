"""Add composite authority keys for Ophthalmology tenant isolation.

Revision ID: aiha_oph_core_scope_20260913
Revises: aiha_pat_audit_scope_20260907
"""

from alembic import op


revision = "aiha_oph_core_scope_20260913"
down_revision = "aiha_pat_audit_scope_20260907"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_hospitals_tenant_id_id",
        "hospitals",
        ["tenant_id", "id"],
    )
    op.create_unique_constraint(
        "uq_patients_hospital_id_id",
        "patients",
        ["hospital_id", "id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_patients_hospital_id_id",
        "patients",
        type_="unique",
    )
    op.drop_constraint(
        "uq_hospitals_tenant_id_id",
        "hospitals",
        type_="unique",
    )
