from __future__ import annotations

import json
import logging
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from fastapi import APIRouter, Request
from opentelemetry import propagate, trace
from opentelemetry.context import Context
from opentelemetry.propagators.textmap import Getter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.trace import (
    SpanKind,
    Status,
    StatusCode,
)
from opentelemetry.trace.propagation.tracecontext import (
    TraceContextTextMapPropagator,
)
from starlette.middleware.base import BaseHTTPMiddleware


SERVICE_NAME = os.getenv(
    "OTEL_SERVICE_NAME",
    "ahos-backend",
)

SERVICE_VERSION = os.getenv(
    "AHOS_SERVICE_VERSION",
    "2.0.0",
)

DEPLOYMENT_ENVIRONMENT = os.getenv(
    "AHOS_ENVIRONMENT",
    "local-development",
)

TRACE_FILE = Path(
    os.getenv(
        "AHOS_TRACE_FILE",
        "logs/ahos_traces.jsonl",
    )
)

OTLP_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
    "",
).strip()

TRACE_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)


router = APIRouter(
    tags=["AHOS Phase 38.3 Distributed Tracing"],
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def trace_id_hex(trace_id: int) -> str:
    return format(trace_id, "032x")


def span_id_hex(span_id: int) -> str:
    return format(span_id, "016x")


class HeaderGetter(Getter):
    def get(
        self,
        carrier: dict[str, str],
        key: str,
    ) -> list[str] | None:
        value = carrier.get(key.lower())

        if value is None:
            return None

        return [value]

    def keys(
        self,
        carrier: dict[str, str],
    ) -> list[str]:
        return list(carrier.keys())


header_getter = HeaderGetter()


class JsonTraceFormatter(logging.Formatter):
    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        payload: dict[str, Any] = {
            "timestamp": utc_now(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        event_data = getattr(
            record,
            "event_data",
            None,
        )

        if isinstance(event_data, dict):
            payload.update(event_data)

        if record.exc_info:
            payload["exception"] = (
                self.formatException(record.exc_info)
            )

        return json.dumps(
            payload,
            ensure_ascii=False,
            default=str,
            separators=(",", ":"),
        )


def build_trace_logger() -> logging.Logger:
    logger = logging.getLogger("ahos.trace")

    if not any(
        getattr(handler, "_ahos_phase38_3", False)
        for handler in logger.handlers
    ):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonTraceFormatter())
        handler._ahos_phase38_3 = True  # type: ignore[attr-defined]
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger


trace_logger = build_trace_logger()


class JsonLineSpanExporter(SpanExporter):
    """
    تصدير التتبعات إلى ملف JSONL محلي.

    لا يتم تسجيل:
    - جسم الطلب
    - جسم الاستجابة
    - بيانات المرضى
    - الرموز السرية أو Authorization headers
    """

    def __init__(
        self,
        output_path: Path,
    ) -> None:
        self.output_path = output_path
        self._lock = threading.Lock()

    def export(
        self,
        spans: Iterable[Any],
    ) -> SpanExportResult:
        records: list[str] = []

        for span in spans:
            context = span.get_span_context()

            parent_span_id = None
            if span.parent is not None:
                parent_span_id = span_id_hex(
                    span.parent.span_id
                )

            events = []

            for event in span.events:
                events.append(
                    {
                        "name": event.name,
                        "timestamp_ns": event.timestamp,
                        "attributes": dict(
                            event.attributes or {}
                        ),
                    }
                )

            payload = {
                "timestamp": utc_now(),
                "service_name": SERVICE_NAME,
                "service_version": SERVICE_VERSION,
                "deployment_environment":
                    DEPLOYMENT_ENVIRONMENT,
                "trace_id": trace_id_hex(
                    context.trace_id
                ),
                "span_id": span_id_hex(
                    context.span_id
                ),
                "parent_span_id": parent_span_id,
                "span_name": span.name,
                "span_kind": str(span.kind),
                "start_time_ns": span.start_time,
                "end_time_ns": span.end_time,
                "duration_ms": round(
                    (
                        span.end_time
                        - span.start_time
                    ) / 1_000_000,
                    3,
                ),
                "status": str(span.status.status_code),
                "status_description":
                    span.status.description,
                "attributes": dict(
                    span.attributes or {}
                ),
                "events": events,
                "resource": dict(
                    span.resource.attributes
                ),
            }

            records.append(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    default=str,
                    separators=(",", ":"),
                )
            )

        if not records:
            return SpanExportResult.SUCCESS

        try:
            with self._lock:
                with self.output_path.open(
                    "a",
                    encoding="utf-8",
                ) as stream:
                    for record in records:
                        stream.write(record)
                        stream.write("\n")

            return SpanExportResult.SUCCESS

        except Exception:
            return SpanExportResult.FAILURE

    def shutdown(self) -> None:
        return None


_tracing_configured = False
_trace_provider: Any = None
_otlp_enabled = False


def configure_tracing() -> Any:
    global _tracing_configured
    global _trace_provider
    global _otlp_enabled

    if _tracing_configured:
        return _trace_provider

    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.version": SERVICE_VERSION,
            "deployment.environment":
                DEPLOYMENT_ENVIRONMENT,
            "ahos.phase": "38.3",
            "telemetry.sdk.language": "python",
        }
    )

    current_provider = trace.get_tracer_provider()

    if (
        current_provider.__class__.__name__
        == "ProxyTracerProvider"
    ):
        provider = TracerProvider(
            resource=resource,
        )
        trace.set_tracer_provider(provider)
    else:
        provider = current_provider

    if not hasattr(
        provider,
        "add_span_processor",
    ):
        raise RuntimeError(
            "Current OpenTelemetry provider does not "
            "support span processors."
        )

    provider.add_span_processor(
        SimpleSpanProcessor(
            JsonLineSpanExporter(
                TRACE_FILE
            )
        )
    )

    if OTLP_ENDPOINT:
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )

            otlp_headers_raw = os.getenv(
                "OTEL_EXPORTER_OTLP_HEADERS",
                "",
            )

            otlp_headers: dict[str, str] = {}

            for item in otlp_headers_raw.split(","):
                item = item.strip()

                if not item or "=" not in item:
                    continue

                key, value = item.split(
                    "=",
                    1,
                )

                otlp_headers[
                    key.strip()
                ] = value.strip()

            exporter = OTLPSpanExporter(
                endpoint=OTLP_ENDPOINT,
                headers=(
                    otlp_headers
                    if otlp_headers
                    else None
                ),
            )

            provider.add_span_processor(
                BatchSpanProcessor(
                    exporter
                )
            )

            _otlp_enabled = True

        except Exception as exc:
            trace_logger.error(
                "otlp_exporter_initialization_failed",
                extra={
                    "event_data": {
                        "event":
                            "otlp_exporter_initialization_failed",
                        "exception_type":
                            type(exc).__name__,
                    }
                },
            )

    propagate.set_global_textmap(
        TraceContextTextMapPropagator()
    )

    _trace_provider = provider
    _tracing_configured = True

    trace_logger.info(
        "tracing_configured",
        extra={
            "event_data": {
                "event": "tracing_configured",
                "service_name": SERVICE_NAME,
                "service_version": SERVICE_VERSION,
                "trace_file": str(TRACE_FILE),
                "otlp_enabled": _otlp_enabled,
                "otlp_endpoint_configured":
                    bool(OTLP_ENDPOINT),
            }
        },
    )

    return provider


configure_tracing()

tracer = trace.get_tracer(
    "ahos.phase38_3",
    SERVICE_VERSION,
)


def normalized_route(
    request: Request,
) -> str:
    route = request.scope.get("route")
    route_path = getattr(
        route,
        "path",
        None,
    )

    if route_path:
        return str(route_path)

    return request.url.path


def current_trace_context() -> dict[str, Any]:
    span = trace.get_current_span()
    context = span.get_span_context()

    if not context.is_valid:
        return {
            "trace_id": None,
            "span_id": None,
            "trace_flags": None,
        }

    return {
        "trace_id": trace_id_hex(
            context.trace_id
        ),
        "span_id": span_id_hex(
            context.span_id
        ),
        "trace_flags": int(
            context.trace_flags
        ),
    }


class Phase38_3OpenTelemetryMiddleware(
    BaseHTTPMiddleware
):
    """
    OpenTelemetry server tracing middleware.

    الوظائف:
    - استخراج traceparent الوارد
    - إنشاء Server Span
    - الحفاظ على Trace ID عبر الخدمات
    - إضافة Trace ID وSpan ID إلى الاستجابة
    - تسجيل الأخطاء والأحداث التشغيلية
    - عدم تسجيل أجسام الطلبات الطبية
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        carrier = {
            key.lower(): value
            for key, value
            in request.headers.items()
        }

        parent_context: Context = (
            propagate.extract(
                carrier=carrier,
                getter=header_getter,
            )
        )

        initial_path = request.url.path
        method = request.method

        correlation_id = (
            request.headers.get(
                "x-correlation-id"
            )
            or request.headers.get(
                "x-request-id"
            )
            or str(uuid.uuid4())
        )

        start = time.perf_counter()

        span_name = (
            f"{method} {initial_path}"
        )

        with tracer.start_as_current_span(
            span_name,
            context=parent_context,
            kind=SpanKind.SERVER,
        ) as span:
            span_context = (
                span.get_span_context()
            )

            trace_id = trace_id_hex(
                span_context.trace_id
            )

            span_id = span_id_hex(
                span_context.span_id
            )

            request.state.trace_id = trace_id
            request.state.span_id = span_id

            span.set_attribute(
                "http.request.method",
                method,
            )
            span.set_attribute(
                "url.path",
                initial_path,
            )
            span.set_attribute(
                "server.address",
                request.url.hostname
                or "unknown",
            )
            span.set_attribute(
                "server.port",
                request.url.port
                or 8000,
            )
            span.set_attribute(
                "ahos.correlation_id",
                correlation_id,
            )
            span.set_attribute(
                "ahos.phase",
                "38.3",
            )

            if request.client:
                span.set_attribute(
                    "client.address",
                    request.client.host,
                )

            try:
                response = await call_next(
                    request
                )

            except Exception as exc:
                duration = (
                    time.perf_counter()
                    - start
                )

                route = normalized_route(
                    request
                )

                span.set_attribute(
                    "http.route",
                    route,
                )
                span.set_attribute(
                    "error.type",
                    type(exc).__name__,
                )
                span.record_exception(exc)
                span.set_status(
                    Status(
                        StatusCode.ERROR,
                        str(exc),
                    )
                )

                trace_logger.exception(
                    "traced_request_failed",
                    extra={
                        "event_data": {
                            "event":
                                "traced_request_failed",
                            "trace_id": trace_id,
                            "span_id": span_id,
                            "correlation_id":
                                correlation_id,
                            "method": method,
                            "route": route,
                            "path": initial_path,
                            "duration_ms": round(
                                duration * 1000,
                                3,
                            ),
                            "exception_type":
                                type(exc).__name__,
                        }
                    },
                )

                raise

            duration = (
                time.perf_counter()
                - start
            )

            route = normalized_route(
                request
            )

            span.update_name(
                f"{method} {route}"
            )

            span.set_attribute(
                "http.route",
                route,
            )
            span.set_attribute(
                "http.response.status_code",
                response.status_code,
            )
            span.set_attribute(
                "ahos.duration_ms",
                round(
                    duration * 1000,
                    3,
                ),
            )

            if response.status_code >= 500:
                span.set_status(
                    Status(
                        StatusCode.ERROR,
                        f"HTTP {response.status_code}",
                    )
                )
            else:
                span.set_status(
                    Status(
                        StatusCode.OK
                    )
                )

            response.headers[
                "X-Trace-ID"
            ] = trace_id

            response.headers[
                "X-Span-ID"
            ] = span_id

            response.headers[
                "X-Trace-Sampled"
            ] = (
                "1"
                if bool(int(span_context.trace_flags) & 0x01)
                else "0"
            )

            trace_logger.info(
                "trace_completed",
                extra={
                    "event_data": {
                        "event":
                            "trace_completed",
                        "trace_id": trace_id,
                        "span_id": span_id,
                        "correlation_id":
                            correlation_id,
                        "method": method,
                        "route": route,
                        "path": initial_path,
                        "status_code":
                            response.status_code,
                        "duration_ms": round(
                            duration * 1000,
                            3,
                        ),
                        "parent_trace_context":
                            bool(
                                request.headers.get(
                                    "traceparent"
                                )
                            ),
                    }
                },
            )

            return response


@router.get(
    "/ahos/38.3/tracing/health"
)
def tracing_health():
    return {
        "status": "healthy",
        "phase": "38.3",
        "component":
            "opentelemetry_distributed_tracing",
        "service_name": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "deployment_environment":
            DEPLOYMENT_ENVIRONMENT,
        "trace_context_format":
            "W3C traceparent",
        "local_jsonl_exporter": "enabled",
        "trace_file": str(TRACE_FILE),
        "otlp_exporter": (
            "enabled"
            if _otlp_enabled
            else "not_configured"
        ),
        "request_body_logging": False,
        "response_body_logging": False,
        "real_patient_data_required": False,
        "clinical_claims": "blocked",
    }


@router.get(
    "/ahos/38.3/tracing/context"
)
def tracing_context():
    context = current_trace_context()

    carrier: dict[str, str] = {}

    propagate.inject(
        carrier=carrier
    )

    return {
        "status": "active",
        **context,
        "outbound_trace_headers": carrier,
    }


@router.get(
    "/ahos/38.3/tracing/child-span-test"
)
def child_span_test():
    parent = current_trace_context()

    with tracer.start_as_current_span(
        "ahos.phase38_3.synthetic_child_span",
        kind=SpanKind.INTERNAL,
    ) as child_span:
        child_span.set_attribute(
            "ahos.synthetic_test",
            True,
        )
        child_span.set_attribute(
            "ahos.real_patient_data",
            False,
        )

        child_span.add_event(
            "synthetic_diagnostic_event",
            {
                "phase": "38.3",
                "safe_test": True,
            },
        )

        child = current_trace_context()

    return {
        "status": "passed",
        "parent_context": parent,
        "child_context": child,
        "same_trace_id": (
            parent["trace_id"]
            == child["trace_id"]
        ),
        "different_span_id": (
            parent["span_id"]
            != child["span_id"]
        ),
        "real_patient_data_used": False,
    }


@router.post(
    "/ahos/38.3/incidents/{incident_id}/correlate"
)
def correlate_incident(
    incident_id: str,
):
    context = current_trace_context()
    span = trace.get_current_span()

    sanitized_incident_id = (
        incident_id.strip()[:128]
    )

    span.set_attribute(
        "ahos.incident_id",
        sanitized_incident_id,
    )

    span.add_event(
        "incident_correlated",
        {
            "incident_id":
                sanitized_incident_id,
            "trace_id":
                context["trace_id"]
                or "",
        },
    )

    trace_logger.info(
        "incident_correlated",
        extra={
            "event_data": {
                "event":
                    "incident_correlated",
                "incident_id":
                    sanitized_incident_id,
                "trace_id":
                    context["trace_id"],
                "span_id":
                    context["span_id"],
                "patient_data_logged": False,
            }
        },
    )

    return {
        "status": "registered",
        "incident_id":
            sanitized_incident_id,
        "trace_id":
            context["trace_id"],
        "span_id":
            context["span_id"],
        "patient_data_logged": False,
    }
