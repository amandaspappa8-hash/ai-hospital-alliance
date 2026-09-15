"""AI HOSPITAL ALLIANCE canonical Alembic environment.

Database migration authority is explicit and fail-closed.

Any Alembic command that requires a database connection must receive:

    AIHA_ALEMBIC_DATABASE_URL

The canonical migration environment intentionally does not inherit a
generic DATABASE_URL and does not construct a migration DSN implicitly
from application runtime settings.
"""

from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from backend.app.ahos_50_0.database import Base
from backend.app.ahos_50_0 import models  # noqa: F401


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _configure_canonical_database_url() -> str:
    """Require and install the explicit canonical migration DSN."""

    database_url = os.getenv(
        "AIHA_ALEMBIC_DATABASE_URL",
        "",
    ).strip()

    if not database_url:
        raise RuntimeError(
            "AIHA_ALEMBIC_DATABASE_URL is required for "
            "canonical AIHA database migration operations."
        )

    # Alembic Config uses ConfigParser interpolation.
    # Literal percent characters in a DSN must therefore be escaped.
    config.set_main_option(
        "sqlalchemy.url",
        database_url.replace("%", "%%"),
    )

    return database_url


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline SQL-generation mode."""

    _configure_canonical_database_url()

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the explicitly authorized database."""

    _configure_canonical_database_url()

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
