"""Add Patient API compatibility columns to canonical patients table.

Revision ID: aiha_pat_api_enrich_20260907
Revises: aiha_pat_tenant_scope_20260906

This migration is intentionally additive only.

It:
- preserves the existing canonical patient varchar primary key,
- preserves all existing foreign keys,
- performs no patient data backfill,
- performs no tenant mapping mutation,
- adds only the Patient API compatibility columns required by Phase 2.7.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "aiha_pat_api_enrich_20260907"
down_revision = "aiha_pat_tenant_scope_20260906"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "patients",
        sa.Column(
            "allergies",
            postgresql.ARRAY(sa.String()),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "blood_type",
            sa.String(length=10),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "chronic_conditions",
            postgresql.ARRAY(sa.String()),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "current_medications",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "date_of_birth",
            sa.Date(),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "full_name",
            sa.String(length=255),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "insurance_provider",
            sa.String(length=255),
            nullable=True,
        ),
        schema="public",
    )

    op.add_column(
        "patients",
        sa.Column(
            "mrn",
            sa.String(length=50),
            nullable=True,
        ),
        schema="public",
    )


def downgrade() -> None:
    op.drop_column(
        "patients",
        "mrn",
        schema="public",
    )

    op.drop_column(
        "patients",
        "insurance_provider",
        schema="public",
    )

    op.drop_column(
        "patients",
        "full_name",
        schema="public",
    )

    op.drop_column(
        "patients",
        "date_of_birth",
        schema="public",
    )

    op.drop_column(
        "patients",
        "current_medications",
        schema="public",
    )

    op.drop_column(
        "patients",
        "chronic_conditions",
        schema="public",
    )

    op.drop_column(
        "patients",
        "blood_type",
        schema="public",
    )

    op.drop_column(
        "patients",
        "allergies",
        schema="public",
    )
