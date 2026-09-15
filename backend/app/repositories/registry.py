from backend.app.repositories.postgres.users_repository import PostgresUsersRepository
from .memory.users_repository import InMemoryUsersRepository
from .memory.patients_repository import InMemoryPatientsRepository
from .postgres.patients_repository import PostgresPatientsRepository
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
from .postgres.labs_repository import PostgresLabsRepository
from .memory.radiology_repository import InMemoryRadiologyRepository
from .postgres.radiology_repository import PostgresRadiologyRepository
from .postgres.mar_repository import PostgresMarRepository
from .memory.doctor_assignments_repository import InMemoryDoctorAssignmentsRepository
from .postgres.doctor_assignments_repository import PostgresDoctorAssignmentsRepository
from backend.app.repositories.postgres.medication_orders_repository import PostgresMedicationOrdersRepository
from backend.app.repositories.postgres.audit_logs_repository import PostgresAuditLogsRepository




_PATIENTS_REPOSITORY = None
_PATIENTS_REPOSITORY_MODE = "legacy_db"


def _build_patients_repository(patients_store):
    """Build the Patient adapter from an isolated transition switch.

    legacy_db remains the default while the historical direct TenantSession
    path is retained by the Patient router. PostgreSQL is explicit opt-in.
    """

    global _PATIENTS_REPOSITORY
    global _PATIENTS_REPOSITORY_MODE

    mode = os.getenv(
        "AIHA_PATIENTS_REPOSITORY",
        "legacy_db",
    ).strip().lower()

    if mode == "legacy_db":
        repository = InMemoryPatientsRepository(
            patients_store
        )
    elif mode == "memory":
        repository = InMemoryPatientsRepository(
            patients_store
        )
    elif mode == "postgres":
        names = {
            "host": "AIHA_PATIENTS_PG_HOST",
            "port": "AIHA_PATIENTS_PG_PORT",
            "database": "AIHA_PATIENTS_PG_DATABASE",
            "username": "AIHA_PATIENTS_PG_USER",
            "password": "AIHA_PATIENTS_PG_PASSWORD",
        }

        values = {
            key: os.getenv(
                env_name,
                "",
            ).strip()
            for key, env_name in names.items()
        }

        missing = [
            names[key]
            for key, value in values.items()
            if not value
        ]

        if missing:
            raise RuntimeError(
                "Missing isolated PostgreSQL Patient configuration: "
                + ", ".join(missing)
            )

        try:
            port = int(values["port"])
        except ValueError as exc:
            raise RuntimeError(
                "AIHA_PATIENTS_PG_PORT must be an integer"
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

        repository = PostgresPatientsRepository(
            engine
        )
    else:
        raise RuntimeError(
            "AIHA_PATIENTS_REPOSITORY must be "
            "'legacy_db', 'postgres', or 'memory'"
        )

    _PATIENTS_REPOSITORY = repository
    _PATIENTS_REPOSITORY_MODE = mode

    return repository


def get_patients_repository():
    if _PATIENTS_REPOSITORY is None:
        raise RuntimeError(
            "Patient repository has not been initialized"
        )

    return _PATIENTS_REPOSITORY


def get_patients_repository_mode() -> str:
    return _PATIENTS_REPOSITORY_MODE


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



def _build_labs_repository(
    labs_catalog_store,
    lab_orders_store,
):
    """Build the AIHA Labs persistence adapter from an isolated feature switch."""

    mode = os.getenv(
        "AIHA_LABS_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode == "memory":
        return InMemoryLabsRepository(
            labs_catalog_store,
            lab_orders_store,
        )

    if mode != "postgres":
        raise RuntimeError(
            "AIHA_LABS_REPOSITORY must be 'memory' or 'postgres'"
        )

    names = {
        "host": "AIHA_LABS_PG_HOST",
        "port": "AIHA_LABS_PG_PORT",
        "database": "AIHA_LABS_PG_DATABASE",
        "username": "AIHA_LABS_PG_USER",
        "password": "AIHA_LABS_PG_PASSWORD",
    }

    values = {
        key: os.getenv(
            env_name,
            "",
        ).strip()
        for key, env_name in names.items()
    }

    missing = [
        names[key]
        for key, value in values.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing AIHA Labs PostgreSQL configuration: "
            + ", ".join(missing)
        )

    try:
        port = int(
            values["port"]
        )
    except ValueError as exc:
        raise RuntimeError(
            "AIHA_LABS_PG_PORT must be an integer"
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

    return PostgresLabsRepository(
        engine,
        labs_catalog_store,
    )


def _build_radiology_repository(
    catalog_store,
    orders_store,
):
    mode = os.getenv(
        "AIHA_RADIOLOGY_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode != "postgres":
        return InMemoryRadiologyRepository(
            catalog_store,
            orders_store,
        )

    host = os.getenv(
        "AIHA_RADIOLOGY_PG_HOST",
        "127.0.0.1",
    )
    port = int(
        os.getenv(
            "AIHA_RADIOLOGY_PG_PORT",
            "5432",
        )
    )
    database = os.getenv(
        "AIHA_RADIOLOGY_PG_DATABASE",
        "aiha_db",
    )
    username = os.getenv(
        "AIHA_RADIOLOGY_PG_USER",
        "postgres",
    )
    password = os.getenv(
        "AIHA_RADIOLOGY_PG_PASSWORD",
        "",
    )

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )

    engine = create_engine(
        url,
        future=True,
        pool_pre_ping=True,
    )

    return PostgresRadiologyRepository(
        engine,
        catalog_store,
    )




def _build_medication_orders_repository():
    """Build the isolated canonical Medication Orders read adapter.

    Default is disabled. PostgreSQL activation is explicit and cannot
    silently inherit the global DATABASE_URL.
    """

    mode = os.getenv(
        "AIHA_MEDICATION_ORDERS_REPOSITORY",
        "disabled",
    ).strip().lower()

    if mode == "disabled":
        return None

    if mode != "postgres":
        raise RuntimeError(
            "AIHA_MEDICATION_ORDERS_REPOSITORY must be "
            "'disabled' or 'postgres'"
        )

    names = {
        "host": "AIHA_MEDICATION_ORDERS_PG_HOST",
        "port": "AIHA_MEDICATION_ORDERS_PG_PORT",
        "database": "AIHA_MEDICATION_ORDERS_PG_DATABASE",
        "username": "AIHA_MEDICATION_ORDERS_PG_USER",
        "password": "AIHA_MEDICATION_ORDERS_PG_PASSWORD",
    }

    values = {
        key: os.getenv(
            env_name,
            "",
        ).strip()
        for key, env_name in names.items()
    }

    missing = [
        names[key]
        for key, value in values.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing isolated PostgreSQL Medication Orders "
            "configuration: "
            + ", ".join(missing)
        )

    try:
        port = int(
            values["port"]
        )
    except ValueError as exc:
        raise RuntimeError(
            "AIHA_MEDICATION_ORDERS_PG_PORT must be an integer"
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

    return PostgresMedicationOrdersRepository(
        engine
    )


def _build_mar_repository(mar_store):
    mode = os.getenv(
        "AIHA_MAR_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode != "postgres":
        return InMemoryMarRepository(
            mar_store or {}
        )

    url = URL.create(
        drivername="postgresql+psycopg2",
        host=os.getenv(
            "AIHA_MAR_PG_HOST",
            "127.0.0.1",
        ),
        port=int(
            os.getenv(
                "AIHA_MAR_PG_PORT",
                "5432",
            )
        ),
        database=os.getenv(
            "AIHA_MAR_PG_DATABASE",
            "aiha_db",
        ),
        username=os.getenv(
            "AIHA_MAR_PG_USER",
            "postgres",
        ),
        password=os.getenv(
            "AIHA_MAR_PG_PASSWORD",
        ),
    )

    engine = create_engine(
        url,
        pool_pre_ping=True,
    )

    return PostgresMarRepository(
        engine
    )



def _build_doctor_assignments_repository(assignments_store):
    mode = os.getenv(
        "AIHA_DOCTOR_ASSIGNMENTS_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode == "memory":
        return InMemoryDoctorAssignmentsRepository(
            assignments_store
        )

    if mode != "postgres":
        raise RuntimeError(
            "Invalid AIHA_DOCTOR_ASSIGNMENTS_REPOSITORY mode"
        )

    env_names = {
        "host": "AIHA_DOCTOR_ASSIGNMENTS_PG_HOST",
        "port": "AIHA_DOCTOR_ASSIGNMENTS_PG_PORT",
        "database": "AIHA_DOCTOR_ASSIGNMENTS_PG_DATABASE",
        "user": "AIHA_DOCTOR_ASSIGNMENTS_PG_USER",
        "password": "AIHA_DOCTOR_ASSIGNMENTS_PG_PASSWORD",
    }

    values = {
        key: os.getenv(env_name)
        for key, env_name in env_names.items()
    }

    missing = [
        env_name
        for key, env_name in env_names.items()
        if not values[key]
    ]

    if missing:
        raise RuntimeError(
            "Missing PostgreSQL configuration for "
            "doctor assignments: "
            + ", ".join(missing)
        )

    try:
        port = int(values["port"])
    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            "Invalid PostgreSQL port for doctor assignments"
        ) from exc

    return PostgresDoctorAssignmentsRepository(
        host=values["host"],
        port=port,
        database=values["database"],
        user=values["user"],
        password=values["password"],
    )



def _build_users_repository(users_store):
    mode = os.getenv(
        "AIHA_USERS_REPOSITORY",
        "memory",
    ).strip().lower()

    if mode in {"memory", "inmemory"}:
        return InMemoryUsersRepository(
            users_store
        )

    if mode not in {"postgres", "postgresql"}:
        raise RuntimeError(
            "Invalid AIHA_USERS_REPOSITORY value"
        )

    environment = {
        "host": os.getenv(
            "AIHA_USERS_PG_HOST"
        ),
        "port": os.getenv(
            "AIHA_USERS_PG_PORT"
        ),
        "database": os.getenv(
            "AIHA_USERS_PG_DATABASE"
        ),
        "user": os.getenv(
            "AIHA_USERS_PG_USER"
        ),
        "password": os.getenv(
            "AIHA_USERS_PG_PASSWORD"
        ),
    }

    missing = [
        key
        for key, value in environment.items()
        if value is None or value == ""
    ]

    if missing:
        raise RuntimeError(
            "Missing isolated PostgreSQL users "
            "repository configuration"
        )

    try:
        port = int(environment["port"])
    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            "Invalid AIHA_USERS_PG_PORT value"
        ) from exc

    return PostgresUsersRepository(
        host=environment["host"],
        port=port,
        database=environment["database"],
        user=environment["user"],
        password=environment["password"],
    )



def _build_audit_logs_repository():
    """Build canonical read-only Audit Logs repository.

    Default is disabled so the existing runtime is not silently changed.

    PostgreSQL activation is explicit and uses an isolated configuration.
    There is deliberately no SQLite fallback.
    """

    mode = os.getenv(
        "AIHA_AUDIT_LOGS_REPOSITORY",
        "disabled",
    ).strip().lower()

    if mode == "disabled":
        return None

    if mode != "postgres":
        raise RuntimeError(
            "AIHA_AUDIT_LOGS_REPOSITORY must be "
            "'disabled' or 'postgres'"
        )

    names = {
        "host": "AIHA_AUDIT_LOGS_PG_HOST",
        "port": "AIHA_AUDIT_LOGS_PG_PORT",
        "database": "AIHA_AUDIT_LOGS_PG_DATABASE",
        "username": "AIHA_AUDIT_LOGS_PG_USER",
        "password": "AIHA_AUDIT_LOGS_PG_PASSWORD",
    }

    values = {
        key: os.getenv(
            env_name,
            "",
        ).strip()
        for key, env_name in names.items()
    }

    missing = [
        names[key]
        for key, value in values.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing isolated PostgreSQL Audit Logs "
            "configuration: "
            + ", ".join(missing)
        )

    try:
        port = int(values["port"])
    except ValueError as exc:
        raise RuntimeError(
            "AIHA_AUDIT_LOGS_PG_PORT must be an integer"
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

    return PostgresAuditLogsRepository(
        engine
    )


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
        "users": _build_users_repository(users_store),
        "patients": _build_patients_repository(patients_store),
        "notes": InMemoryNotesRepository(notes_store),
        "orders": InMemoryOrdersRepository(orders_store),
        "appointments": _build_appointments_repository(appointments_store or []),
        "reports": InMemoryReportsRepository(reports_store or []),
        "nursing": _build_nursing_repository(
            nursing_vitals_store or {},
            nursing_notes_store or {},
        ),
        "medication_orders": _build_medication_orders_repository(),
        "audit_logs": _build_audit_logs_repository(),
        "mar": _build_mar_repository(mar_store or {}),
        "labs": _build_labs_repository(labs_catalog_store or {}, lab_orders_store or []),
        "radiology": _build_radiology_repository(radiology_catalog_store or {}, radiology_orders_store or []),
        "doctor_assignments": _build_doctor_assignments_repository(doctor_assignments_store or {}),
    }
