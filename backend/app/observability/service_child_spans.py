from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator
from urllib.parse import urlsplit

import httpx
from opentelemetry import trace
from opentelemetry.trace import (
    SpanKind,
    Status,
    StatusCode,
)

def _safe_target(url: str) -> dict[str, Any]:
    """
    Returns operational destination metadata only.

    Query strings, response bodies, FHIR resources,
    DICOM tags, patient identifiers, accession numbers,
    and authentication values are deliberately excluded.
    """
    parsed = urlsplit(url)

    return {
        "server.address": parsed.hostname or "",
        "server.port": parsed.port or (
            443 if parsed.scheme == "https" else 80
        ),
        "url.scheme": parsed.scheme,
        "url.path": parsed.path,
        "url.query.recorded": False,
    }


def _phase39_4_runtime():
    """
    Lazy import prevents a module-level circular import.
    """
    module = __import__(
        "backend.app.observability.phase39_4",
        fromlist=[
            "get_phase39_4_server_span_context",
            "get_phase39_4_tracer",
        ],
    )

    return module


def _parent_context() -> Any:
    module = _phase39_4_runtime()

    server_context = (
        module.get_phase39_4_server_span_context()
    )

    if server_context.is_valid:
        parent_span = trace.NonRecordingSpan(
            server_context
        )

        return trace.set_span_in_context(
            parent_span
        )

    current_span = trace.get_current_span()
    current_context = (
        current_span.get_span_context()
    )

    if current_context.is_valid:
        return trace.set_span_in_context(
            current_span
        )

    return None


@contextmanager
def service_span(
    *,
    name: str,
    layer: str,
    operation: str,
    destination_url: str,
) -> Iterator[Any]:
    runtime = _phase39_4_runtime()

    tracer = runtime.get_phase39_4_tracer(
        f"ahos.{layer}",
        "39.5.6R",
    )

    attributes = {
        "ahos.phase": "39.5.6",
        "ahos.telemetry.layer": layer,
        "ahos.operation": operation,
        "ahos.patient_data_included": False,
        "ahos.clinical_payload_recorded": False,
        "http.request.body.recorded": False,
        "http.response.body.recorded": False,
        **_safe_target(destination_url),
    }

    span = tracer.start_span(
        name,
        context=_parent_context(),
        kind=SpanKind.CLIENT,
        attributes=attributes,
    )

    scope = trace.use_span(
        span,
        end_on_exit=False,
    )

    scope.__enter__()

    try:
        yield span

        span.set_status(
            Status(StatusCode.OK)
        )

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


async def traced_json_get(
    *,
    name: str,
    layer: str,
    operation: str,
    url: str,
    timeout_seconds: float = 5.0,
) -> dict[str, Any]:
    with service_span(
        name=name,
        layer=layer,
        operation=operation,
        destination_url=url,
    ) as span:
        async with httpx.AsyncClient(
            timeout=timeout_seconds,
            follow_redirects=False,
            trust_env=False,
        ) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": (
                        "AHOS-Phase39.5.6-"
                        "Observability-Probe"
                    ),
                    "Accept": "application/json",
                },
            )

        span.set_attribute(
            "http.request.method",
            "GET",
        )

        span.set_attribute(
            "http.response.status_code",
            response.status_code,
        )

        span.set_attribute(
            "network.protocol.name",
            "http",
        )

        response.raise_for_status()

        try:
            payload = response.json()

        except Exception:
            payload = {
                "response_format": "non-json",
            }

        return {
            "status_code": response.status_code,
            "payload": payload,
        }
