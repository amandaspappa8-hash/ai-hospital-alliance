from datetime import (
    datetime,
    timedelta,
    timezone,
)

from backend.app.services.core.tenant_lifecycle_authority_service import (
    TenantLifecycleAuthorityService,
)


NOW = datetime(
    2026,
    9,
    20,
    8,
    0,
    0,
    tzinfo=timezone.utc,
)

PAST = NOW - timedelta(days=1)
FUTURE = NOW + timedelta(days=1)


def base_record():
    return {
        "tenant_id": "TEN-1",
        "lifecycle_state": "PURGE_PENDING",
        "legal_hold_active": False,
        "retention_until": PAST,
        "offboarding_approved_at": PAST,
        "archive_completed_at": PAST,
        "purge_eligible_at": PAST,
    }


def evaluate(record):
    return (
        TenantLifecycleAuthorityService
        .evaluate_record(
            record=record,
            evaluation_time=NOW,
        )
    )


def test_missing_authority_is_blocked():
    decision = evaluate(None)

    assert decision.code == (
        "BLOCKED_MISSING_LIFECYCLE_AUTHORITY"
    )
    assert (
        decision.eligible_for_destructive_review
        is False
    )
    assert decision.execution_authorized is False


def test_legal_hold_is_blocked():
    record = base_record()
    record["legal_hold_active"] = True

    assert evaluate(record).code == (
        "BLOCKED_LEGAL_HOLD"
    )


def test_missing_retention_is_blocked():
    record = base_record()
    record["retention_until"] = None

    assert evaluate(record).code == (
        "BLOCKED_MISSING_RETENTION_AUTHORITY"
    )


def test_unexpired_retention_is_blocked():
    record = base_record()
    record["retention_until"] = FUTURE

    assert evaluate(record).code == (
        "BLOCKED_RETENTION_ACTIVE"
    )


def test_missing_offboarding_approval_is_blocked():
    record = base_record()
    record["offboarding_approved_at"] = None

    assert evaluate(record).code == (
        "BLOCKED_OFFBOARDING_NOT_APPROVED"
    )


def test_missing_archive_completion_is_blocked():
    record = base_record()
    record["archive_completed_at"] = None

    assert evaluate(record).code == (
        "BLOCKED_ARCHIVE_NOT_COMPLETED"
    )


def test_missing_purge_eligibility_time_is_blocked():
    record = base_record()
    record["purge_eligible_at"] = None

    assert evaluate(record).code == (
        "BLOCKED_MISSING_PURGE_ELIGIBILITY_TIME"
    )


def test_future_purge_eligibility_time_is_blocked():
    record = base_record()
    record["purge_eligible_at"] = FUTURE

    assert evaluate(record).code == (
        "BLOCKED_PURGE_ELIGIBILITY_TIME_NOT_REACHED"
    )


def test_state_other_than_purge_pending_is_blocked():
    record = base_record()
    record["lifecycle_state"] = "ARCHIVED"

    assert evaluate(record).code == (
        "BLOCKED_LIFECYCLE_STATE"
    )


def test_unknown_state_is_blocked():
    record = base_record()
    record["lifecycle_state"] = "UNKNOWN"

    assert evaluate(record).code == (
        "BLOCKED_LIFECYCLE_STATE"
    )


def test_all_gates_pass_is_review_only():
    decision = evaluate(
        base_record()
    )

    assert decision.code == (
        "ELIGIBLE_FOR_DESTRUCTIVE_REVIEW"
    )

    assert (
        decision.eligible_for_destructive_review
        is True
    )

    assert decision.execution_authorized is False


def test_naive_evaluation_time_fails_closed():
    decision = (
        TenantLifecycleAuthorityService
        .evaluate_record(
            record=base_record(),
            evaluation_time=datetime(
                2026,
                9,
                20,
                8,
                0,
                0,
            ),
        )
    )

    assert decision.code == (
        "BLOCKED_INVALID_LIFECYCLE_AUTHORITY"
    )


def test_naive_authority_timestamp_fails_closed():
    record = base_record()

    record["retention_until"] = datetime(
        2026,
        9,
        19,
        8,
        0,
        0,
    )

    assert evaluate(record).code == (
        "BLOCKED_INVALID_LIFECYCLE_AUTHORITY"
    )


def test_malformed_legal_hold_fails_closed():
    record = base_record()
    record["legal_hold_active"] = "false"

    assert evaluate(record).code == (
        "BLOCKED_INVALID_LIFECYCLE_AUTHORITY"
    )


def test_service_reads_once_then_evaluates():
    class Repository:
        def __init__(self):
            self.calls = []

        def get_by_tenant_id(
            self,
            *,
            tenant_id,
            connection=None,
        ):
            self.calls.append(
                (
                    tenant_id,
                    connection,
                )
            )

            return None

    repository = Repository()

    service = TenantLifecycleAuthorityService(
        repository
    )

    marker = object()

    decision = service.evaluate(
        tenant_id="TEN-1",
        evaluation_time=NOW,
        connection=marker,
    )

    assert repository.calls == [
        (
            "TEN-1",
            marker,
        )
    ]

    assert decision.code == (
        "BLOCKED_MISSING_LIFECYCLE_AUTHORITY"
    )

    assert decision.execution_authorized is False
