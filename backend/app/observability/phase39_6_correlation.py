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
    Counter,
    Histogram,
    REGISTRY,
)
from prometheus_client.openmetrics.exposition import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CORRELATION_LOG = (
    PROJECT_ROOT
    / "logs"
    / "ahos_phase39_6_correlation.jsonl"
)

_WRITE_LOCK = Lock()


def _get_or_create_counter():
    name = "ahos_phase39_6_correlated_requests_total"

    try:
        return Counter(
            name,
            (
                "AHOS Phase 39.6 requests correlated "
                "across logs, metrics and traces."
            ),
            labelnames=(
                "phase",
                "operation",
                "status",
            ),
        )
    except ValueError:
        return REGISTRY._names_to_collectors[name]


def _get_or_create_histogram():
    name = "ahos_phase39_6_correlation_duration_seconds"

    try:
        return Histogram(
            name,
            (
                "AHOS Phase 39.6 unified correlation "
                "processing duration."
            ),
            labelnames=(
                "phase",
                "operation",
            ),
            buckets=(
                0.001,
                0.005,
                0.01,
                0.025,
                0.05,
                0.1,
                0.25,
                0.5,
                1.0,
            ),
        )
    except ValueError:
        return REGISTRY._names_to_collectors[name]


CORRELATED_REQUESTS = _get_or_create_counter()
CORRELATION_DURATION = _get_or_create_histogram()


def _phase39_4_runtime():
    """
    Lazy import prevents circular imports and guarantees
    use of the same tracer provider and server context.
    """
    return __import__(
        "backend.app.observability.phase39_4",
        fromlist=[
            "get_phase39_4_server_span_context",
            "get_phase39_4_tracer",
        ],
    )


def _ids() -> tuple[str, str]:
    runtime = _phase39_4_runtime()

    context = (
        runtime
        .get_phase39_4_server_span_context()
    )

    if not context.is_valid:
        current = trace.get_current_span()
        context = current.get_span_context()

    if not context.is_valid:
        return "", ""

    return (
        format(context.trace_id, "032x"),
        format(context.span_id, "016x"),
    )


def _parent_context():
    runtime = _phase39_4_runtime()

    context = (
        runtime
        .get_phase39_4_server_span_context()
    )

    if not context.is_valid:
        return None

    parent = trace.NonRecordingSpan(context)

    return trace.set_span_in_context(parent)


def _write_log(payload: dict[str, Any]) -> None:
    CORRELATION_LOG.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with _WRITE_LOCK:
        with CORRELATION_LOG.open(
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


async def _push_to_loki(
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    Sends only sanitized operational correlation data.
    No clinical payload, FHIR content, DICOM tags,
    patient identifiers, bodies or query strings.
    """
    timestamp_ns = str(time.time_ns())

    loki_payload = {
        "streams": [
            {
                "stream": {
                    "job": "ahos-backend",
                    "service": "ahos-backend",
                    "phase": "39.6",
                    "kind": "unified-correlation",
                },
                "values": [
                    [
                        timestamp_ns,
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


async def execute_correlation_probe(
    correlation_id: str,
) -> dict[str, Any]:
    started = time.perf_counter()

    runtime = _phase39_4_runtime()

    tracer = runtime.get_phase39_4_tracer(
        "ahos.phase39_6.correlation",
        "39.6",
    )

    span = tracer.start_span(
        "AHOS correlation.unified",
        context=_parent_context(),
        kind=SpanKind.INTERNAL,
        attributes={
            "ahos.phase": "39.6",
            "ahos.telemetry.layer": "correlation",
            "ahos.correlation_id": correlation_id,
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
        context = span.get_span_context()

        trace_id = (
            format(context.trace_id, "032x")
            if context.is_valid
            else ""
        )

        child_span_id = (
            format(context.span_id, "016x")
            if context.is_valid
            else ""
        )

        root_trace_id, root_span_id = _ids()

        event = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "phase": "39.6",
            "event": "unified_correlation_probe",
            "service_name": "ahos-backend",
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "root_trace_id": root_trace_id,
            "root_span_id": root_span_id,
            "correlation_span_id": child_span_id,
            "operation": "correlation-probe",
            "status": "PASSED",
            "patient_data_included": False,
            "clinical_payload_recorded": False,
        }

        _write_log(event)

        labels = CORRELATED_REQUESTS.labels(
            phase="39.6",
            operation="correlation-probe",
            status="PASSED",
        )

        exemplar = {
            "trace_id": trace_id,
            "correlation_id": correlation_id,
        }

        exemplar_recorded = True

        try:
            labels.inc(exemplar=exemplar)
        except TypeError:
            labels.inc()
            exemplar_recorded = False

        loki = await _push_to_loki(event)

        duration = (
            time.perf_counter() - started
        )

        CORRELATION_DURATION.labels(
            phase="39.6",
            operation="correlation-probe",
        ).observe(duration)

        span.set_attribute(
            "ahos.log.file_written",
            True,
        )
        span.set_attribute(
            "ahos.metric.counter_incremented",
            True,
        )
        span.set_attribute(
            "ahos.metric.exemplar_recorded",
            exemplar_recorded,
        )
        span.set_attribute(
            "ahos.loki.push_success",
            bool(loki.get("success")),
        )

        span.set_status(
            Status(StatusCode.OK)
        )

        return {
            "phase": "39.6",
            "status": "PASSED",
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "root_trace_id": root_trace_id,
            "root_span_id": root_span_id,
            "correlation_span_id": child_span_id,
            "same_trace_id": (
                trace_id == root_trace_id
                and bool(trace_id)
            ),
            "structured_log_written": True,
            "prometheus_counter_incremented": True,
            "prometheus_exemplar_recorded": (
                exemplar_recorded
            ),
            "loki": loki,
            "duration_seconds": duration,
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


def phase39_6_metrics_response() -> Response:
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )
