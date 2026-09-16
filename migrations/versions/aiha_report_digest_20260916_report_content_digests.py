"""Create canonical report content digest baseline table.

SEC-S4E16D

This table stores a SHA-256 digest of server-derived canonical report
content. It does not represent a digital signature, blockchain record,
immutable-ledger proof, clinical approval, regulatory approval, or
identity certification.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aiha_report_digest_20260916"
down_revision: Union[str, None] = "aiha_report_verify_evt_20260915"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "report_content_digests",
        sa.Column(
            "id",
            sa.BigInteger(),
            sa.Identity(
                always=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "report_id",
            sa.String(
                length=20,
            ),
            nullable=False,
        ),
        sa.Column(
            "canonicalization_version",
            sa.String(
                length=40,
            ),
            nullable=False,
        ),
        sa.Column(
            "digest_algorithm",
            sa.String(
                length=20,
            ),
            nullable=False,
        ),
        sa.Column(
            "digest_hex",
            sa.String(
                length=64,
            ),
            nullable=False,
        ),
        sa.Column(
            "secured_by_user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "secured_at",
            sa.DateTime(
                timezone=True,
            ),
            server_default=sa.text(
                "now()"
            ),
            nullable=False,
        ),
        sa.CheckConstraint(
            "canonicalization_version = "
            "'AIHA_REPORT_DIGEST_V1'",
            name=(
                "ck_report_content_digests_"
                "canonicalization_version"
            ),
        ),
        sa.CheckConstraint(
            "digest_algorithm = 'SHA-256'",
            name=(
                "ck_report_content_digests_"
                "digest_algorithm"
            ),
        ),
        sa.CheckConstraint(
            "digest_hex ~ '^[0-9a-f]{64}$'",
            name=(
                "ck_report_content_digests_"
                "digest_hex"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["report_id"],
            ["reports.id"],
            name=(
                "fk_report_content_digests_"
                "report_id_reports"
            ),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["secured_by_user_id"],
            ["users.id"],
            name=(
                "fk_report_content_digests_"
                "secured_by_user_id_users"
            ),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_report_content_digests",
        ),
        sa.UniqueConstraint(
            "report_id",
            "canonicalization_version",
            name=(
                "uq_report_content_digests_"
                "report_version"
            ),
        ),
    )

    op.create_index(
        "ix_report_content_digests_"
        "secured_by_user_id",
        "report_content_digests",
        ["secured_by_user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_report_content_digests_"
        "secured_by_user_id",
        table_name="report_content_digests",
    )

    op.drop_table(
        "report_content_digests"
    )
