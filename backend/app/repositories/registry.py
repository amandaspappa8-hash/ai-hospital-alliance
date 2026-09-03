from .memory.users_repository import InMemoryUsersRepository
from .memory.patients_repository import InMemoryPatientsRepository
from .memory.notes_repository import InMemoryNotesRepository
from .memory.orders_repository import InMemoryOrdersRepository
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from .memory.appointments_repository import InMemoryAppointmentsRepository
from .postgres.appointments_repository import PostgresAppointmentsRepository
from .postgres.nursing_repository import PostgresNursingRepository
from .memory.reports_repository import InMemoryReportsRepository
from .memory.nursing_repository import InMemoryNursingRepository
from .memory.mar_repository import InMemoryMarRepository
from .memory.labs_repository import InMemoryLabsRepository
from .memory.radiology_repository import InMemoryRadiologyRepository
from .memory.doctor_assignments_repository import InMemoryDoctorAssignmentsRepository



def _build_appointments_repository(appointments_store):
    """
    Select the appointments persistence adapter.

    Default is intentionally memory to preserve the established
    AHOS runtime baseline until PostgreSQL activation is explicitly
    authorized.

    PostgreSQL appointments configuration is isolated from the global
    DATABASE_URL so this pilot cannot silently switch unrelated AHOS
    persistence layers.
    """

    mode = os.getenv(
        "AHOS_APPOINTMENTS_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode == "memory":
        return InMemoryAppointmentsRepository(
            appointments_store
        )

    if mode != "postgres":
        raise RuntimeError(
            "Invalid AHOS_APPOINTMENTS_REPOSITORY. "
            "Expected 'memory' or 'postgres'."
        )

    names = {
        "host": "AHOS_APPOINTMENTS_PG_HOST",
        "port": "AHOS_APPOINTMENTS_PG_PORT",
        "database": "AHOS_APPOINTMENTS_PG_DATABASE",
        "username": "AHOS_APPOINTMENTS_PG_USER",
        "password": "AHOS_APPOINTMENTS_PG_PASSWORD",
    }

    values = {
        key: os.getenv(env_name, "").strip()
        for key, env_name in names.items()
    }

    missing = [
        names[key]
        for key, value in values.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing PostgreSQL appointments configuration: "
            + ", ".join(missing)
        )

    try:
        port = int(values["port"])
    except ValueError as exc:
        raise RuntimeError(
            "AHOS_APPOINTMENTS_PG_PORT must be an integer"
        ) from exc

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=values["username"],
        password=values["password"],
        host=values["host"],
        port=port,
        database=values["database"],
    )

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        pool_recycle=3600,
    )

    return PostgresAppointmentsRepository(
        engine
    )

def _build_nursing_repository(
    nursing_vitals_store,
    nursing_notes_store,
):
    """Build Nursing repository from an isolated feature switch."""
    mode = os.getenv(
        "AHOS_NURSING_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode == "memory":
        return InMemoryNursingRepository(
            nursing_vitals_store,
            nursing_notes_store,
        )

    if mode != "postgres":
        raise RuntimeError(
            "AHOS_NURSING_REPOSITORY must be "
            "'memory' or 'postgres'"
        )

    required = {
        "host": os.getenv("AHOS_NURSING_PG_HOST"),
        "port": os.getenv("AHOS_NURSING_PG_PORT"),
        "database": os.getenv("AHOS_NURSING_PG_DATABASE"),
        "username": os.getenv("AHOS_NURSING_PG_USER"),
        "password": os.getenv("AHOS_NURSING_PG_PASSWORD"),
    }

    missing = [
        key
        for key, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing Nursing PostgreSQL configuration: "
            + ", ".join(sorted(missing))
        )

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=required["username"],
        password=required["password"],
        host=required["host"],
        port=int(required["port"]),
        database=required["database"],
    )

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=300,
    )

    return PostgresNursingRepository(engine)


def build_repositories(
    users_store,
    patients_store,
    notes_store,
    orders_store,
    appointments_store=None,
    reports_store=None,
    nursing_vitals_store=None,
    nursing_notes_store=None,
    mar_store=None,
    labs_catalog_store=None,
    lab_orders_store=None,
    radiology_catalog_store=None,
    radiology_orders_store=None,
    doctor_assignments_store=None,
):
    return {
        "users": InMemoryUsersRepository(users_store),
        "patients": InMemoryPatientsRepository(patients_store),
        "notes": InMemoryNotesRepository(notes_store),
        "orders": InMemoryOrdersRepository(orders_store),
        "appointments": _build_appointments_repository(appointments_store or []),
        "reports": InMemoryReportsRepository(reports_store or []),
        "nursing": _build_nursing_repository(
            nursing_vitals_store or {},
            nursing_notes_store or {},
        ),
        "mar": InMemoryMarRepository(mar_store or {}),
        "labs": InMemoryLabsRepository(
            labs_catalog_store or {}, lab_orders_store or []
        ),
        "radiology": InMemoryRadiologyRepository(
            radiology_catalog_store or {}, radiology_orders_store or []
        ),
        "doctor_assignments": InMemoryDoctorAssignmentsRepository(
            doctor_assignments_store or {}
        ),
    }
