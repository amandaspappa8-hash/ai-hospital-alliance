from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

import httpx
from fastapi.responses import Response
from opentelemetry import trace
from opentelemetry.trace import (
    SpanKind,
    Status,
    StatusCode,
)
from prometheus_client import (
    Gauge,
    REGISTRY,
)
from prometheus_client.openmetrics.exposition import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

INCIDENT_LOG = (
    PROJECT_ROOT
    / "logs"
    / "ahos_phase39_7_incidents.jsonl"
)

WEBHOOK_LOG = (
    PROJECT_ROOT
    / "logs"
    / "ahos_phase39_7_alertmanager.jsonl"
)

_WRITE_LOCK = Lock()

_STATE: dict[str, Any] = {
    "active": False,
    "incident_id": "",
    "correlation_id": "",
    "trace_id": "",
    "root_span_id": "",
    "incident_span_id": "",
    "availability_ratio": 1.0,
    "latency_p95_seconds": 0.15,
    "updated_at": "",
}


def _get_or_create_gauge(
    name: str,
    documentation: str,
    labels: tuple[str, ...],
):
    try:
        return Gauge(
            name,
            documentation,
            labelnames=labels,
        )
    except ValueError:
        return REGISTRY._names_to_collectors[name]


INCIDENT_ACTIVE = _get_or_create_gauge(
    "ahos_phase39_7_incident_active",
    "Whether the AHOS Phase 39.7 synthetic incident is active.",
    (
        "phase",
        "incident_id",
        "correlation_id",
        "trace_id",
    ),
)

AVAILABILITY_RATIO = _get_or_create_gauge(
    "ahos_phase39_7_availability_ratio",
    "AHOS Phase 39.7 operational availability SLI.",
    (
        "phase",
        "service",
    ),
)

LATENCY_P95 = _get_or_create_gauge(
    "ahos_phase39_7_latency_p95_seconds",
    "AHOS Phase 39.7 p95 request latency SLI.",
    (
        "phase",
        "service",
    ),
)


def _runtime():
    return __import__(
        "backend.app.observability.phase39_4",
        fromlist=[
            "get_phase39_4_server_span_context",
            "get_phase39_4_tracer",
        ],
    )


def _root_context():
    context = (
        _runtime()
        .get_phase39_4_server_span_context()
    )

    return context


def _write_json_line(
    path: Path,
    payload: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with _WRITE_LOCK:
        with path.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(
                    payload,
                    separators=(",", ":"),
                    ensure_ascii=False,
                )
                + "\n"
            )


async def _push_loki(
    payload: dict[str, Any],
) -> dict[str, Any]:
    loki_payload = {
        "streams": [
            {
                "stream": {
                    "job": "ahos-backend",
                    "service": "ahos-backend",
                    "phase": "39.7",
                    "kind": "incident-correlation",
                },
                "values": [
                    [
                        str(time.time_ns()),
                        json.dumps(
                            payload,
                            separators=(",", ":"),
                            ensure_ascii=False,
                        ),
                    ]
                ],
            }
        ]
    }

    try:
        async with httpx.AsyncClient(
            timeout=5.0,
            trust_env=False,
        ) as client:
            response = await client.post(
                (
                    "http://127.0.0.1:3100"
                    "/loki/api/v1/push"
                ),
                json=loki_payload,
            )

        return {
            "available": True,
            "status_code": response.status_code,
            "success": response.status_code in {
                200,
                204,
            },
        }

    except Exception as exc:
        return {
            "available": False,
            "status_code": 0,
            "success": False,
            "error_type": type(exc).__name__,
        }


def _clear_incident_gauge() -> None:
    try:
        INCIDENT_ACTIVE.clear()
    except Exception:
        pass


async def simulate_incident(
    *,
    active: bool,
    incident_id: str,
    correlation_id: str,
) -> dict[str, Any]:
    runtime = _runtime()
    root_context = _root_context()

    parent_context = None

    if root_context.is_valid:
        parent_context = trace.set_span_in_context(
            trace.NonRecordingSpan(
                root_context
            )
        )

    tracer = runtime.get_phase39_4_tracer(
        "ahos.phase39_7.incident",
        "39.7",
    )

    span = tracer.start_span(
        (
            "AHOS incident.activated"
            if active
            else "AHOS incident.resolved"
        ),
        context=parent_context,
        kind=SpanKind.INTERNAL,
        attributes={
            "ahos.phase": "39.7",
            "ahos.telemetry.layer": "incident",
            "ahos.incident.id": incident_id,
            "ahos.correlation_id": correlation_id,
            "ahos.incident.active": active,
            "ahos.patient_data_included": False,
            "ahos.clinical_payload_recorded": False,
        },
    )

    scope = trace.use_span(
        span,
        end_on_exit=False,
    )

    scope.__enter__()

    try:
        span_context = span.get_span_context()

        trace_id = (
            format(
                span_context.trace_id,
                "032x",
            )
            if span_context.is_valid
            else ""
        )

        incident_span_id = (
            format(
                span_context.span_id,
                "016x",
            )
            if span_context.is_valid
            else ""
        )

        root_span_id = (
            format(
                root_context.span_id,
                "016x",
            )
            if root_context.is_valid
            else ""
        )

        availability = 0.98 if active else 1.0
        latency = 1.20 if active else 0.15

        _clear_incident_gauge()

        INCIDENT_ACTIVE.labels(
            phase="39.7",
            incident_id=incident_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
        ).set(
            1 if active else 0
        )

        AVAILABILITY_RATIO.labels(
            phase="39.7",
            service="ahos-backend",
        ).set(availability)

        LATENCY_P95.labels(
            phase="39.7",
            service="ahos-backend",
        ).set(latency)

        now = datetime.now(
            timezone.utc
        ).isoformat()

        _STATE.update(
            {
                "active": active,
                "incident_id": incident_id,
                "correlation_id": correlation_id,
                "trace_id": trace_id,
                "root_span_id": root_span_id,
                "incident_span_id": incident_span_id,
                "availability_ratio": availability,
                "latency_p95_seconds": latency,
                "updated_at": now,
            }
        )

        event = {
            "timestamp": now,
            "phase": "39.7",
            "event": (
                "operational_incident_activated"
                if active
                else "operational_incident_resolved"
            ),
            "status": (
                "FIRING"
                if active
                else "RESOLVED"
            ),
            "incident_id": incident_id,
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "root_span_id": root_span_id,
            "incident_span_id": incident_span_id,
            "availability_ratio": availability,
            "latency_p95_seconds": latency,
            "patient_data_included": False,
            "clinical_payload_recorded": False,
        }

        _write_json_line(
            INCIDENT_LOG,
            event,
        )

        loki = await _push_loki(event)

        span.set_attribute(
            "ahos.sli.availability_ratio",
            availability,
        )
        span.set_attribute(
            "ahos.sli.latency_p95_seconds",
            latency,
        )
        span.set_attribute(
            "ahos.loki.push_success",
            bool(loki.get("success")),
        )

        span.set_status(
            Status(StatusCode.OK)
        )

        return {
            "phase": "39.7",
            "status": (
                "FIRING"
                if active
                else "RESOLVED"
            ),
            "incident_active": active,
            "incident_id": incident_id,
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "root_span_id": root_span_id,
            "incident_span_id": incident_span_id,
            "availability_ratio": availability,
            "latency_p95_seconds": latency,
            "loki": loki,
            "real_patient_data_used": False,
            "clinical_payload_recorded": False,
        }

    except Exception as exc:
        span.record_exception(exc)

        span.set_status(
            Status(
                StatusCode.ERROR,
                type(exc).__name__,
            )
        )

        raise

    finally:
        scope.__exit__(
            None,
            None,
            None,
        )
        span.end()


def metrics_response() -> Response:
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )


def incident_status() -> dict[str, Any]:
    return {
        "phase": "39.7",
        "status": "ACTIVE",
        "incident": dict(_STATE),
        "slos": {
            "availability_target": 0.999,
            "latency_p95_target_seconds": 0.5,
        },
        "real_patient_data_used": False,
        "clinical_payload_recorded": False,
    }


def record_alertmanager_webhook(
    payload: dict[str, Any],
) -> dict[str, Any]:
    sanitized_alerts = []

    for alert in payload.get(
        "alerts",
        [],
    ):
        labels = alert.get(
            "labels",
            {},
        )

        annotations = alert.get(
            "annotations",
            {},
        )

        sanitized_alerts.append(
            {
                "status": alert.get("status"),
                "labels": {
                    "alertname": labels.get(
                        "alertname"
                    ),
                    "severity": labels.get(
                        "severity"
                    ),
                    "phase": labels.get("phase"),
                    "service": labels.get(
                        "service"
                    ),
                    "incident_id": labels.get(
                        "incident_id"
                    ),
                    "correlation_id": labels.get(
                        "correlation_id"
                    ),
                    "trace_id": labels.get(
                        "trace_id"
                    ),
                },
                "annotations": {
                    "summary": annotations.get(
                        "summary"
                    ),
                    "description": annotations.get(
                        "description"
                    ),
                },
                "startsAt": alert.get("startsAt"),
                "endsAt": alert.get("endsAt"),
            }
        )

    event = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "phase": "39.7",
        "event": "alertmanager_webhook_received",
        "receiver": payload.get("receiver"),
        "status": payload.get("status"),
        "alerts": sanitized_alerts,
        "patient_data_included": False,
        "clinical_payload_recorded": False,
    }

    _write_json_line(
        WEBHOOK_LOG,
        event,
    )

    return {
        "status": "ACCEPTED",
        "alerts_received": len(
            sanitized_alerts
        ),
        "real_patient_data_used": False,
    }


AVAILABILITY_RATIO.labels(
    phase="39.7",
    service="ahos-backend",
).set(1.0)

LATENCY_P95.labels(
    phase="39.7",
    service="ahos-backend",
).set(0.15)
