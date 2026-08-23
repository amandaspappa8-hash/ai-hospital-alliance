from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.middleware.base import BaseHTTPMiddleware


router = APIRouter(
    tags=["AHOS Phase 38.2 Runtime Observability"],
)


HTTP_REQUESTS_TOTAL = Counter(
    "ahos_http_requests_total",
    "Total number of HTTP requests processed by AHOS.",
    ["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "ahos_http_request_duration_seconds",
    "AHOS HTTP request duration in seconds.",
    ["method", "route"],
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0,
    ),
)

HTTP_EXCEPTIONS_TOTAL = Counter(
    "ahos_http_exceptions_total",
    "Total unhandled HTTP request exceptions.",
    ["method", "route", "exception_type"],
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "ahos_http_requests_in_progress",
    "Number of AHOS HTTP requests currently being processed.",
    ["method"],
)


class JsonFormatter(logging.Formatter):
    """Minimal structured JSON formatter for AHOS runtime events."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        event_data = getattr(record, "event_data", None)
        if isinstance(event_data, dict):
            payload.update(event_data)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(
            payload,
            ensure_ascii=False,
            default=str,
            separators=(",", ":"),
        )


def build_runtime_logger() -> logging.Logger:
    logger = logging.getLogger("ahos.runtime")

    if not any(
        getattr(handler, "_ahos_phase38_2", False)
        for handler in logger.handlers
    ):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        handler._ahos_phase38_2 = True  # type: ignore[attr-defined]
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


runtime_logger = build_runtime_logger()


def _normalized_route(request: Request) -> str:
    route = request.scope.get("route")
    route_path = getattr(route, "path", None)

    if route_path:
        return str(route_path)

    return request.url.path


class Phase38_2RuntimeObservabilityMiddleware(BaseHTTPMiddleware):
    """
    AHOS Phase 38.2 middleware.

    Provides:
    - Request and correlation identifiers
    - Structured JSON runtime logs
    - Request counters
    - Latency histograms
    - In-progress request gauge
    - Exception counters
    """

    async def dispatch(self, request: Request, call_next):
        request_id = (
            request.headers.get("x-request-id")
            or str(uuid.uuid4())
        )
        correlation_id = (
            request.headers.get("x-correlation-id")
            or request_id
        )

        request.state.request_id = request_id
        request.state.correlation_id = correlation_id

        method = request.method
        initial_path = request.url.path
        start = time.perf_counter()

        HTTP_REQUESTS_IN_PROGRESS.labels(method=method).inc()

        try:
            response = await call_next(request)

        except Exception as exc:
            duration = time.perf_counter() - start
            route = _normalized_route(request)

            HTTP_EXCEPTIONS_TOTAL.labels(
                method=method,
                route=route,
                exception_type=type(exc).__name__,
            ).inc()

            runtime_logger.exception(
                "request_failed",
                extra={
                    "event_data": {
                        "event": "request_failed",
                        "request_id": request_id,
                        "correlation_id": correlation_id,
                        "method": method,
                        "route": route,
                        "path": initial_path,
                        "duration_ms": round(duration * 1000, 3),
                        "exception_type": type(exc).__name__,
                    }
                },
            )
            raise

        finally:
            HTTP_REQUESTS_IN_PROGRESS.labels(method=method).dec()

        duration = time.perf_counter() - start
        route = _normalized_route(request)
        status_code = str(response.status_code)

        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            route=route,
            status_code=status_code,
        ).inc()

        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=method,
            route=route,
        ).observe(duration)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Response-Time-MS"] = f"{duration * 1000:.3f}"

        # نتجنب تسجيل محتوى البيانات الطبية أو جسم الطلب.
        if initial_path != "/metrics":
            runtime_logger.info(
                "request_completed",
                extra={
                    "event_data": {
                        "event": "request_completed",
                        "request_id": request_id,
                        "correlation_id": correlation_id,
                        "method": method,
                        "route": route,
                        "path": initial_path,
                        "status_code": int(status_code),
                        "duration_ms": round(duration * 1000, 3),
                        "client": (
                            request.client.host
                            if request.client
                            else None
                        ),
                    }
                },
            )

        return response


@router.get(
    "/metrics",
    include_in_schema=False,
)
def prometheus_metrics() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@router.get("/ahos/38.2/observability/health")
def phase38_2_observability_health():
    return {
        "status": "healthy",
        "phase": "38.2",
        "component": "runtime_metrics_and_json_logging",
        "prometheus_metrics": "enabled",
        "structured_json_logging": "enabled",
        "request_id": "enabled",
        "correlation_id": "enabled",
        "request_duration": "enabled",
        "medical_request_bodies_logged": False,
        "clinical_claims": "blocked",
    }
