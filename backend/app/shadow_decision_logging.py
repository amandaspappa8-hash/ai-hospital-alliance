"""
AHOS Phase 40.2.4.14
Persistent live shadow-decision writer and mismatch metrics.

Privacy controls:
- No access tokens.
- No Authorization headers.
- No request or response payloads.
- No query strings.
- Variable path segments are redacted.
"""

from __future__ import annotations

import json
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_LOG_DIRECTORY = _PROJECT_ROOT / "logs" / "security"

_DECISION_LOG = (
    _LOG_DIRECTORY / "shadow_decisions.jsonl"
)

_METRICS_FILE = (
    _LOG_DIRECTORY / "shadow_metrics.json"
)

_LOCK = threading.RLock()

_UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-"
    r"[0-9a-fA-F]{12}$"
)

_LONG_IDENTIFIER_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]{13,}$"
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize_path(path: str) -> str:
    """
    Remove likely record, patient, report and UUID identifiers
    from path segments before persistence.
    """

    clean_path = (path or "/").split("?", 1)[0]
    segments: list[str] = []

    for segment in clean_path.split("/"):
        if not segment:
            continue

        replace_segment = (
            segment.isdigit()
            or bool(_UUID_PATTERN.fullmatch(segment))
            or bool(
                _LONG_IDENTIFIER_PATTERN.fullmatch(
                    segment
                )
            )
        )

        segments.append(
            "{id}"
            if replace_segment
            else segment[:80]
        )

    return "/" + "/".join(segments)


def _empty_metrics() -> dict[str, Any]:
    return {
        "phase": "AHOS Phase 40.2.4.14",
        "updated_at": _timestamp(),
        "total_decisions": 0,
        "matches": 0,
        "mismatches": 0,
        "match_ratio": None,
        "runtime_classifications": {
            "PUBLIC": 0,
            "PROTECTED": 0,
            "ADMIN": 0,
            "OTHER": 0,
        },
        "approved_classifications": {
            "PUBLIC": 0,
            "PROTECTED": 0,
            "ADMIN": 0,
            "OTHER": 0,
        },
        "transitions": {},
        "privacy": {
            "tokens_logged": False,
            "authorization_headers_logged": False,
            "query_strings_logged": False,
            "request_payloads_logged": False,
            "response_payloads_logged": False,
            "path_identifiers_redacted": True,
        },
        "enforcement": {
            "shadow_mode": True,
            "blocking_enabled": False,
            "default_deny_enabled": False,
        },
    }


def _read_metrics() -> dict[str, Any]:
    if not _METRICS_FILE.is_file():
        return _empty_metrics()

    try:
        payload = json.loads(
            _METRICS_FILE.read_text(
                encoding="utf-8"
            )
        )

        if isinstance(payload, dict):
            return payload

    except (OSError, ValueError, TypeError):
        pass

    return _empty_metrics()


def _write_metrics_atomic(
    metrics: dict[str, Any],
) -> None:
    temporary = _METRICS_FILE.with_suffix(
        ".json.tmp"
    )

    temporary.write_text(
        json.dumps(
            metrics,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    temporary.replace(_METRICS_FILE)


def initialize_shadow_logging() -> None:
    with _LOCK:
        _LOG_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not _DECISION_LOG.exists():
            _DECISION_LOG.touch()

        if not _METRICS_FILE.exists():
            _write_metrics_atomic(
                _empty_metrics()
            )


def record_shadow_decision(
    *,
    path: str,
    method: str,
    runtime_classification: str,
    approved_classification: str,
) -> dict[str, Any]:
    initialize_shadow_logging()

    runtime_class = (
        runtime_classification
        if runtime_classification
        in {"PUBLIC", "PROTECTED", "ADMIN"}
        else "OTHER"
    )

    approved_class = (
        approved_classification
        if approved_classification
        in {"PUBLIC", "PROTECTED", "ADMIN"}
        else "OTHER"
    )

    matched = runtime_class == approved_class

    record = {
        "timestamp": _timestamp(),
        "method": str(method or "UNKNOWN").upper(),
        "path": _sanitize_path(path),
        "runtime_classification": runtime_class,
        "approved_classification": approved_class,
        "matched": matched,
    }

    with _LOCK:
        with _DECISION_LOG.open(
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            )

        metrics = _read_metrics()

        metrics["total_decisions"] = (
            int(
                metrics.get(
                    "total_decisions",
                    0,
                )
            )
            + 1
        )

        if matched:
            metrics["matches"] = (
                int(metrics.get("matches", 0))
                + 1
            )
        else:
            metrics["mismatches"] = (
                int(
                    metrics.get(
                        "mismatches",
                        0,
                    )
                )
                + 1
            )

        for key, classification in (
            (
                "runtime_classifications",
                runtime_class,
            ),
            (
                "approved_classifications",
                approved_class,
            ),
        ):
            counters = metrics.setdefault(
                key,
                {},
            )

            counters[classification] = (
                int(
                    counters.get(
                        classification,
                        0,
                    )
                )
                + 1
            )

        transition = (
            f"{runtime_class}_TO_"
            f"{approved_class}"
        )

        transitions = metrics.setdefault(
            "transitions",
            {},
        )

        transitions[transition] = (
            int(
                transitions.get(
                    transition,
                    0,
                )
            )
            + 1
        )

        total = int(
            metrics.get(
                "total_decisions",
                0,
            )
        )

        matches = int(
            metrics.get(
                "matches",
                0,
            )
        )

        metrics["match_ratio"] = (
            round(matches / total, 6)
            if total
            else None
        )

        metrics["updated_at"] = _timestamp()

        _write_metrics_atomic(metrics)

    return record


def get_shadow_metrics() -> dict[str, Any]:
    initialize_shadow_logging()

    with _LOCK:
        metrics = _read_metrics()

        return json.loads(
            json.dumps(metrics)
        )


def get_recent_shadow_decisions(
    limit: int = 20,
) -> list[dict[str, Any]]:
    initialize_shadow_logging()

    safe_limit = max(
        1,
        min(int(limit), 100),
    )

    with _LOCK:
        try:
            lines = _DECISION_LOG.read_text(
                encoding="utf-8"
            ).splitlines()
        except OSError:
            return []

    records: list[dict[str, Any]] = []

    for line in lines[-safe_limit:]:
        try:
            payload = json.loads(line)

            if isinstance(payload, dict):
                records.append(payload)

        except (ValueError, TypeError):
            continue

    return records


initialize_shadow_logging()
