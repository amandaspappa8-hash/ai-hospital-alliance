"""Add canonical report content MAC baseline storage.

Revision ID: aiha_report_mac_20260916
Revises: aiha_report_digest_20260916
Create Date: 2026-09-16

This migration provides persistence only.

It does not establish:
- asymmetric digital signatures
- individual signer identity
- PKI / certificate authority
- non-repudiation
- eIDAS qualification
- FDA Part 11 certification
- blockchain notarization
"""

from alembic import op
import sqlalchemy as sa


revision: str = "aiha_report_mac_20260916"
down_revision: str | None = "aiha_report_digest_20260916"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "report_content_macs",

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
            "mac_version",
            sa.String(length=40),
            nullable=False,
        ),

        sa.Column(
            "mac_algorithm",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "mac_hex",
            sa.String(length=64),
            nullable=False,
        ),

        sa.Column(
            "created_by_user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.CheckConstraint(
            "mac_version = 'AIHA_REPORT_CONTENT_MAC_V1'",
            name="ck_report_content_macs_version",
        ),

        sa.CheckConstraint(
            "mac_algorithm = 'HMAC-SHA256'",
            name="ck_report_content_macs_algorithm",
        ),

        sa.CheckConstraint(
            "mac_hex ~ '^[0-9a-f]{64}$'",
            name="ck_report_content_macs_hex",
        ),

        sa.ForeignKeyConstraint(
            ["report_id"],
            ["public.reports.id"],
            name="fk_report_content_macs_report_id",
            ondelete="RESTRICT",
        ),

        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["public.users.id"],
            name="fk_report_content_macs_created_by_user_id",
            ondelete="RESTRICT",
        ),

        sa.PrimaryKeyConstraint(
            "id",
            name="pk_report_content_macs",
        ),

        sa.UniqueConstraint(
            "report_id",
            "mac_version",
            name="uq_report_content_macs_report_version",
        ),

        schema="public",
    )

    op.create_index(
        "ix_report_content_macs_created_by_user_id",
        "report_content_macs",
        ["created_by_user_id"],
        unique=False,
        schema="public",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_report_content_macs_created_by_user_id",
        table_name="report_content_macs",
        schema="public",
    )

    op.drop_table(
        "report_content_macs",
        schema="public",
    )
