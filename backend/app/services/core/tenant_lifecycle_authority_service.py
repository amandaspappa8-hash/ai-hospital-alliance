from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from backend.app.repositories.contracts.tenant_lifecycle_authority_repository import (
    TenantLifecycleAuthorityRepositoryContract,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LifecycleAuthorityDecision:
    code: str
    eligible_for_destructive_review: bool
    execution_authorized: bool = False


class TenantLifecycleAuthorityService:
    """Fail-closed lifecycle authority policy.

    ELIGIBLE_FOR_DESTRUCTIVE_REVIEW is a review outcome only.
    This service does not authorize or execute destructive operations.
    """

    BLOCKED_MISSING_LIFECYCLE_AUTHORITY = (
        "BLOCKED_MISSING_LIFECYCLE_AUTHORITY"
    )
    BLOCKED_LEGAL_HOLD = (
        "BLOCKED_LEGAL_HOLD"
    )
    BLOCKED_MISSING_RETENTION_AUTHORITY = (
        "BLOCKED_MISSING_RETENTION_AUTHORITY"
    )
    BLOCKED_RETENTION_ACTIVE = (
        "BLOCKED_RETENTION_ACTIVE"
    )
    BLOCKED_OFFBOARDING_NOT_APPROVED = (
        "BLOCKED_OFFBOARDING_NOT_APPROVED"
    )
    BLOCKED_ARCHIVE_NOT_COMPLETED = (
        "BLOCKED_ARCHIVE_NOT_COMPLETED"
    )
    BLOCKED_MISSING_PURGE_ELIGIBILITY_TIME = (
        "BLOCKED_MISSING_PURGE_ELIGIBILITY_TIME"
    )
    BLOCKED_PURGE_ELIGIBILITY_TIME_NOT_REACHED = (
        "BLOCKED_PURGE_ELIGIBILITY_TIME_NOT_REACHED"
    )
    BLOCKED_LIFECYCLE_STATE = (
        "BLOCKED_LIFECYCLE_STATE"
    )
    BLOCKED_INVALID_LIFECYCLE_AUTHORITY = (
        "BLOCKED_INVALID_LIFECYCLE_AUTHORITY"
    )
    ELIGIBLE_FOR_DESTRUCTIVE_REVIEW = (
        "ELIGIBLE_FOR_DESTRUCTIVE_REVIEW"
    )

    def __init__(
        self,
        repository: TenantLifecycleAuthorityRepositoryContract,
    ) -> None:
        self.repository = repository

    @classmethod
    def _blocked(
        cls,
        code: str,
    ) -> LifecycleAuthorityDecision:
        return LifecycleAuthorityDecision(
            code=code,
            eligible_for_destructive_review=False,
            execution_authorized=False,
        )

    @classmethod
    def _eligible(
        cls,
    ) -> LifecycleAuthorityDecision:
        return LifecycleAuthorityDecision(
            code=(
                cls.ELIGIBLE_FOR_DESTRUCTIVE_REVIEW
            ),
            eligible_for_destructive_review=True,
            execution_authorized=False,
        )

    @staticmethod
    def _is_aware_datetime(
        value: Any,
    ) -> bool:
        return (
            isinstance(value, datetime)
            and value.tzinfo is not None
            and value.utcoffset() is not None
        )

    @classmethod
    def evaluate_record(
        cls,
        *,
        record: dict[str, Any] | None,
        evaluation_time: datetime,
    ) -> LifecycleAuthorityDecision:
        """Evaluate lifecycle authority without database access or mutation."""

        if not cls._is_aware_datetime(
            evaluation_time
        ):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        if record is None:
            return cls._blocked(
                cls.BLOCKED_MISSING_LIFECYCLE_AUTHORITY
            )

        if not isinstance(record, dict):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        legal_hold = record.get(
            "legal_hold_active"
        )

        if not isinstance(
            legal_hold,
            bool,
        ):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        if legal_hold:
            return cls._blocked(
                cls.BLOCKED_LEGAL_HOLD
            )

        retention_until = record.get(
            "retention_until"
        )

        if retention_until is None:
            return cls._blocked(
                cls.BLOCKED_MISSING_RETENTION_AUTHORITY
            )

        if not cls._is_aware_datetime(
            retention_until
        ):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        if retention_until > evaluation_time:
            return cls._blocked(
                cls.BLOCKED_RETENTION_ACTIVE
            )

        offboarding_approved_at = record.get(
            "offboarding_approved_at"
        )

        if offboarding_approved_at is None:
            return cls._blocked(
                cls.BLOCKED_OFFBOARDING_NOT_APPROVED
            )

        if not cls._is_aware_datetime(
            offboarding_approved_at
        ):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        archive_completed_at = record.get(
            "archive_completed_at"
        )

        if archive_completed_at is None:
            return cls._blocked(
                cls.BLOCKED_ARCHIVE_NOT_COMPLETED
            )

        if not cls._is_aware_datetime(
            archive_completed_at
        ):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        purge_eligible_at = record.get(
            "purge_eligible_at"
        )

        if purge_eligible_at is None:
            return cls._blocked(
                cls.BLOCKED_MISSING_PURGE_ELIGIBILITY_TIME
            )

        if not cls._is_aware_datetime(
            purge_eligible_at
        ):
            return cls._blocked(
                cls.BLOCKED_INVALID_LIFECYCLE_AUTHORITY
            )

        if purge_eligible_at > evaluation_time:
            return cls._blocked(
                cls.BLOCKED_PURGE_ELIGIBILITY_TIME_NOT_REACHED
            )

        lifecycle_state = record.get(
            "lifecycle_state"
        )

        if (
            not isinstance(
                lifecycle_state,
                str,
            )
            or lifecycle_state != "PURGE_PENDING"
        ):
            return cls._blocked(
                cls.BLOCKED_LIFECYCLE_STATE
            )

        return cls._eligible()

    def evaluate(
        self,
        *,
        tenant_id: str,
        evaluation_time: datetime,
        connection: Any | None = None,
    ) -> LifecycleAuthorityDecision:
        record = self.repository.get_by_tenant_id(
            tenant_id=tenant_id,
            connection=connection,
        )

        return self.evaluate_record(
            record=record,
            evaluation_time=evaluation_time,
        )
