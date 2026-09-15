"""Create canonical report verification events table.

Revision ID: aiha_report_verify_evt_20260915
Revises: aiha_reports_summary_20260915
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aiha_report_verify_evt_20260915"
down_revision: Union[str, Sequence[str], None] = "aiha_reports_summary_20260915"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "report_verification_events",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(),
            nullable=False,
        ),
        sa.Column(
            "report_id",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "verification_type",
            sa.String(length=40),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=40),
            nullable=False,
        ),
        sa.Column(
            "verified_by_user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "verified_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "verification_type IN ('REGISTRATION')",
            name="ck_report_verification_events_type",
        ),
        sa.CheckConstraint(
            "status IN ('REGISTERED')",
            name="ck_report_verification_events_status",
        ),
        sa.ForeignKeyConstraint(
            ["report_id"],
            ["reports.id"],
            name="fk_report_verification_events_report_id_reports",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["verified_by_user_id"],
            ["users.id"],
            name="fk_report_verification_events_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_report_verification_events",
        ),
        sa.UniqueConstraint(
            "report_id",
            "verification_type",
            name="uq_report_verification_events_report_type",
        ),
        schema="public",
    )

    op.create_index(
        "ix_report_verification_events_verified_by_user_id",
        "report_verification_events",
        ["verified_by_user_id"],
        unique=False,
        schema="public",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_report_verification_events_verified_by_user_id",
        table_name="report_verification_events",
        schema="public",
    )

    op.drop_table(
        "report_verification_events",
        schema="public",
    )
