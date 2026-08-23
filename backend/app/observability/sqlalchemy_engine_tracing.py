from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from opentelemetry import trace
from opentelemetry.trace import (
    SpanKind,
    Status,
    StatusCode,
)
from sqlalchemy import event
from sqlalchemy.engine import Engine

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DIAGNOSTIC_LOG = (
    PROJECT_ROOT
    / "logs"
    / "ahos_phase39_5_5_db_events.jsonl"
)

_STACK_KEY = "_ahos_phase39_5_span_stack"
_INSTALLED_ATTRIBUTE = "_ahos_phase39_5_events_installed"
_WRITE_LOCK = Lock()

_SQL_OPERATION = re.compile(
    r"^\s*(SELECT|INSERT|UPDATE|DELETE|"
    r"CREATE|ALTER|DROP|PRAGMA|WITH|"
    r"BEGIN|COMMIT|ROLLBACK|REPLACE)",
    re.IGNORECASE,
)


def _hex_trace_id(span: Any) -> str:
    context = span.get_span_context()

    if not context.is_valid:
        return ""

    return format(context.trace_id, "032x")


def _hex_span_id(span: Any) -> str:
    context = span.get_span_context()

    if not context.is_valid:
        return ""

    return format(context.span_id, "016x")


def _operation(statement: Any) -> str:
    match = _SQL_OPERATION.match(
        str(statement or "")
    )

    if not match:
        return "QUERY"

    return match.group(1).upper()


def _fingerprint(statement: Any) -> str:
    normalized = " ".join(
        str(statement or "").split()
    )

    return hashlib.sha256(
        normalized.encode(
            "utf-8",
            errors="replace",
        )
    ).hexdigest()[:16]


def _write_event(payload: dict[str, Any]) -> None:
    DIAGNOSTIC_LOG.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    with _WRITE_LOCK:
        with DIAGNOSTIC_LOG.open(
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


def install_sqlalchemy_engine_tracing(
    engine: Engine,
    tracer_provider: Any,
) -> dict[str, Any]:
    if getattr(
        engine,
        _INSTALLED_ATTRIBUTE,
        False,
    ):
        return {
            "status": "ALREADY_INSTALLED",
            "engine": type(engine).__name__,
        }

    tracer = tracer_provider.get_tracer(
        "ahos.sqlalchemy.engine",
        "39.5.5D",
    )

    db_system = str(
        getattr(
            engine.url,
            "drivername",
            "sqlalchemy",
        )
    ).split("+", 1)[0]

    def before_cursor_execute(
        conn: Any,
        cursor: Any,
        statement: Any,
        parameters: Any,
        context: Any,
        executemany: bool,
    ) -> None:
        operation = _operation(statement)

        current_span = trace.get_current_span()
        current_context = (
            current_span.get_span_context()
        )

        server_context = (
            (
            __import__(
                "backend.app.observability.phase39_4",
                fromlist=[
                    "get_phase39_4_server_span_context"
                ],
            )
            .get_phase39_4_server_span_context()
        )
        )

        if server_context.is_valid:
            parent_span = trace.NonRecordingSpan(
                server_context
            )
        else:
            parent_span = current_span

        parent_context = trace.set_span_in_context(
            parent_span
        )

        span = tracer.start_span(
            f"{operation} {db_system}",
            context=parent_context,
            kind=SpanKind.CLIENT,
            attributes={
                "db.system": db_system,
                "db.operation": operation,
                "db.query.fingerprint": (
                    _fingerprint(statement)
                ),
                "db.query.text_recorded": False,
                "db.bind_values_recorded": False,
                "ahos.phase": "39.5.5D",
                "ahos.telemetry.layer": "database",
                "ahos.patient_data_included": False,
            },
        )

        scope = trace.use_span(
            span,
            end_on_exit=False,
        )

        scope.__enter__()

        conn.info.setdefault(
            _STACK_KEY,
            [],
        ).append(
            {
                "span": span,
                "scope": scope,
            }
        )

        _write_event(
            {
                "event": "before_cursor_execute",
                "operation": operation,
                "db_system": db_system,
                "server_trace_id": (
                    format(
                        server_context.trace_id,
                        "032x",
                    )
                    if server_context.is_valid
                    else ""
                ),
                "server_span_id": (
                    format(
                        server_context.span_id,
                        "016x",
                    )
                    if server_context.is_valid
                    else ""
                ),
                "server_context_valid": (
                    server_context.is_valid
                ),
                "current_trace_id": (
                    format(
                        current_context.trace_id,
                        "032x",
                    )
                    if current_context.is_valid
                    else ""
                ),
                "current_span_id": (
                    format(
                        current_context.span_id,
                        "016x",
                    )
                    if current_context.is_valid
                    else ""
                ),
                "current_span_recording": (
                    current_span.is_recording()
                ),
                "database_trace_id": (
                    _hex_trace_id(span)
                ),
                "database_span_id": (
                    _hex_span_id(span)
                ),
                "database_span_recording": (
                    span.is_recording()
                ),
                "database_span_sampled": (
                    span.get_span_context()
                    .trace_flags.sampled
                ),
            }
        )

    def after_cursor_execute(
        conn: Any,
        cursor: Any,
        statement: Any,
        parameters: Any,
        context: Any,
        executemany: bool,
    ) -> None:
        stack = conn.info.get(
            _STACK_KEY,
            [],
        )

        if not stack:
            _write_event(
                {
                    "event": "after_cursor_execute",
                    "error": "SPAN_STACK_EMPTY",
                }
            )
            return

        item = stack.pop()
        span = item["span"]
        scope = item["scope"]

        trace_id = _hex_trace_id(span)
        span_id = _hex_span_id(span)

        try:
            rowcount = getattr(
                cursor,
                "rowcount",
                None,
            )

            if isinstance(rowcount, int):
                span.set_attribute(
                    "db.response.row_count",
                    rowcount,
                )

            span.set_status(
                Status(StatusCode.OK)
            )

        finally:
            scope.__exit__(
                None,
                None,
                None,
            )
            span.end()

            _write_event(
                {
                    "event": "after_cursor_execute",
                    "database_trace_id": trace_id,
                    "database_span_id": span_id,
                    "span_ended": True,
                }
            )

    def handle_error(
        exception_context: Any,
    ) -> None:
        connection = getattr(
            exception_context,
            "connection",
            None,
        )

        if connection is None:
            return

        stack = connection.info.get(
            _STACK_KEY,
            [],
        )

        if not stack:
            return

        item = stack.pop()
        span = item["span"]
        scope = item["scope"]

        exception = getattr(
            exception_context,
            "original_exception",
            None,
        )

        try:
            if exception is not None:
                span.record_exception(exception)

            span.set_status(
                Status(
                    StatusCode.ERROR,
                    type(exception).__name__
                    if exception is not None
                    else "DatabaseError",
                )
            )

        finally:
            scope.__exit__(
                None,
                None,
                None,
            )
            span.end()

            _write_event(
                {
                    "event": "handle_error",
                    "database_trace_id": (
                        _hex_trace_id(span)
                    ),
                    "database_span_id": (
                        _hex_span_id(span)
                    ),
                    "exception_type": (
                        type(exception).__name__
                        if exception is not None
                        else "DatabaseError"
                    ),
                }
            )

    event.listen(
        engine,
        "before_cursor_execute",
        before_cursor_execute,
    )

    event.listen(
        engine,
        "after_cursor_execute",
        after_cursor_execute,
    )

    event.listen(
        engine,
        "handle_error",
        handle_error,
    )

    setattr(
        engine,
        _INSTALLED_ATTRIBUTE,
        True,
    )

    return {
        "status": "INSTALLED",
        "engine": type(engine).__name__,
        "db_system": db_system,
        "diagnostic_log": str(DIAGNOSTIC_LOG),
        "events": [
            "before_cursor_execute",
            "after_cursor_execute",
            "handle_error",
        ],
        "sql_text_recorded": False,
        "bind_values_recorded": False,
    }
