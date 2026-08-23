from __future__ import annotations

import json
import logging
import os
import time
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.trace import (
    INVALID_SPAN_CONTEXT,
    SpanContext,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from backend.app.observability.sqlalchemy_engine_tracing import install_sqlalchemy_engine_tracing
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = PROJECT_ROOT / "logs"
REQUEST_LOG = LOG_DIR / "ahos_phase39_4_requests.jsonl"

SERVICE_NAME = os.getenv(
    "OTEL_SERVICE_NAME",
    "ahos-backend",
)

OTLP_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
    "http://127.0.0.1:4318/v1/traces",
)

_CORRELATION_ID: ContextVar[str] = ContextVar(
    "ahos_phase39_4_correlation_id",
    default="",
)

_INSTALL_LOCK = Lock()
_INSTALLED = False
_PHASE39_4_TRACER_PROVIDER = None


_PHASE39_4_SERVER_SPAN_CONTEXT: ContextVar[SpanContext] = (
    ContextVar(
        "ahos_phase39_4_server_span_context",
        default=INVALID_SPAN_CONTEXT,
    )
)


def get_phase39_4_server_span_context() -> SpanContext:
    """
    Returns the FastAPI server-span context for the
    current request.

    Database and external-service instrumentation use
    this context to join the same end-to-end trace.
    """
    return _PHASE39_4_SERVER_SPAN_CONTEXT.get()


def _phase39_4_server_trace_id() -> str:
    context = get_phase39_4_server_span_context()

    if not context.is_valid:
        return ""

    return format(context.trace_id, "032x")


def _phase39_4_server_span_id() -> str:
    context = get_phase39_4_server_span_context()

    if not context.is_valid:
        return ""

    return format(context.span_id, "016x")



def _trace_id() -> str:
    server_trace_id = _phase39_4_server_trace_id()

    if server_trace_id:
        return server_trace_id

    span = trace.get_current_span()
    context = span.get_span_context()

    if not context.is_valid:
        return ""

    return format(context.trace_id, "032x")


def _span_id() -> str:
    server_span_id = _phase39_4_server_span_id()

    if server_span_id:
        return server_span_id

    span = trace.get_current_span()
    context = span.get_span_context()

    if not context.is_valid:
        return ""

    return format(context.span_id, "016x")


def _write_request_log(payload: dict[str, Any]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with REQUEST_LOG.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        )


def _build_tracer_provider() -> TracerProvider:
    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.namespace": "ahos",
            "service.version": "39.4",
            "deployment.environment.name": os.getenv(
                "AHOS_ENVIRONMENT",
                "local-production-validation",
            ),
            "ahos.phase": "39.4",
            "ahos.platform": "AI Hospital Alliance",
        }
    )

    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(
        endpoint=OTLP_ENDPOINT,
        timeout=15,
    )

    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )

    return provider


class Phase39_4CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        incoming_id = (
            request.headers.get("x-correlation-id")
            or request.headers.get("x-request-id")
            or ""
        ).strip()

        correlation_id = incoming_id or str(uuid.uuid4())
        token = _CORRELATION_ID.set(correlation_id)

        start_time = time.perf_counter()
        response: Response | None = None
        status_code = 500
        error_type = ""

        try:
            current_span = trace.get_current_span()

            if current_span.is_recording():
                current_span.set_attribute(
                    "ahos.correlation_id",
                    correlation_id,
                )
                current_span.set_attribute(
                    "ahos.phase",
                    "39.4",
                )
                current_span.set_attribute(
                    "ahos.patient_data_included",
                    False,
                )

            response = await call_next(request)
            status_code = response.status_code

            return response

        except Exception as exc:
            error_type = type(exc).__name__

            current_span = trace.get_current_span()

            if current_span.is_recording():
                current_span.record_exception(exc)

            raise

        finally:
            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            trace_id = _trace_id()
            span_id = _span_id()

            route = request.scope.get("route")
            route_path = getattr(
                route,
                "path",
                request.url.path,
            )

            payload = {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "service_name": SERVICE_NAME,
                "service_version": "39.4",
                "phase": "39.4",
                "correlation_id": correlation_id,
                "request_id": correlation_id,
                "trace_id": trace_id,
                "span_id": span_id,
                "http_method": request.method,
                "http_route": route_path,
                "http_target": request.url.path,
                "http_status_code": status_code,
                "duration_ms": round(duration_ms, 3),
                "error_type": error_type,
                "patient_data_included": False,
            }

            _write_request_log(payload)

            if response is not None:
                response.headers[
                    "X-Correlation-ID"
                ] = correlation_id

                if trace_id:
                    response.headers[
                        "X-Trace-ID"
                    ] = trace_id

                if span_id:
                    response.headers[
                        "X-Span-ID"
                    ] = span_id

            _CORRELATION_ID.reset(token)


def _server_request_hook(
    span: Any,
    scope: dict[str, Any],
) -> None:
    if span is None or not span.is_recording():
        return

    span_context = span.get_span_context()

    if span_context.is_valid:
        _PHASE39_4_SERVER_SPAN_CONTEXT.set(
            span_context
        )

    span.set_attribute("ahos.phase", "39.4")
    span.set_attribute(
        "ahos.platform",
        "AI Hospital Alliance",
    )
    span.set_attribute(
        "ahos.patient_data_included",
        False,
    )

    headers = {
        key.decode("latin-1").lower():
        value.decode("latin-1")
        for key, value in scope.get("headers", [])
    }

    correlation_id = (
        headers.get("x-correlation-id")
        or headers.get("x-request-id")
        or ""
    )

    if correlation_id:
        span.set_attribute(
            "ahos.incoming_correlation_id",
            correlation_id,
        )



def get_phase39_4_tracer(
    instrumentation_name: str,
    instrumentation_version: str = "39.5.6R",
):
    """
    Returns a tracer from the exact provider used by
    Phase 39.4 FastAPI instrumentation.
    """
    if _PHASE39_4_TRACER_PROVIDER is None:
        raise RuntimeError(
            "Phase 39.4 tracer provider is unavailable."
        )

    return _PHASE39_4_TRACER_PROVIDER.get_tracer(
        instrumentation_name,
        instrumentation_version,
    )


def install_phase39_4(app: FastAPI) -> dict[str, Any]:
    global _INSTALLED
    global _PHASE39_4_TRACER_PROVIDER

    with _INSTALL_LOCK:
        if _INSTALLED:
            return {
                "status": "ALREADY_INSTALLED",
                "service_name": SERVICE_NAME,
            }

        provider = _build_tracer_provider()
        _PHASE39_4_TRACER_PROVIDER = provider

        app.add_middleware(
            Phase39_4CorrelationMiddleware
        )

        FastAPIInstrumentor.instrument_app(
            app,
            tracer_provider=provider,
            server_request_hook=_server_request_hook,
            excluded_urls="/metrics",
        )

        from backend.app.db.database import engine

        sqlalchemy_engine_tracing = (
            install_sqlalchemy_engine_tracing(
                engine=engine,
                tracer_provider=provider,
            )
        )


        state = {
            "status": "INSTALLED",
            "service_name": SERVICE_NAME,
            "otlp_endpoint": OTLP_ENDPOINT,
            "request_log": str(REQUEST_LOG),
            "automatic_fastapi_instrumentation": True,
            "sqlalchemy_engine_tracing": sqlalchemy_engine_tracing,
            "request_correlation": True,
            "response_headers": [
                "X-Correlation-ID",
                "X-Trace-ID",
                "X-Span-ID",
            ],
        }

        app.state.ahos_phase39_4 = state
        _INSTALLED = True

        return dict(state)
