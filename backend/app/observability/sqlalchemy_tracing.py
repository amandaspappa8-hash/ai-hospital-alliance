from contextlib import contextmanager
from opentelemetry import trace

tracer = trace.get_tracer("ahos.sqlalchemy")

@contextmanager
def sqlalchemy_span(operation: str, table: str | None = None):
    with tracer.start_as_current_span(
        f"sqlalchemy.{operation}"
    ) as span:

        span.set_attribute(
            "db.system",
            "sqlalchemy"
        )

        span.set_attribute(
            "db.operation",
            operation
        )

        if table:
            span.set_attribute(
                "db.sql.table",
                table
            )

        yield span
