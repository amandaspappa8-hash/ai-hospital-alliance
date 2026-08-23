import argparse
import os
import sys
import uuid
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SQLITE_URL = os.getenv("SQLITE_URL", "sqlite:///./hospital.db")
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://aiha:aiha123@localhost:5432/aiha_db")

ALEMBIC_ENV = '''
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.models import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''

ALEMBIC_INI = """[alembic]
script_location = migrations
sqlalchemy.url = postgresql://aiha:aiha123@localhost:5432/aiha_db

[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARN
handlers = console
qualname =
[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = [sys.stderr,]
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %%H:%%M:%%S
"""


def setup_alembic():
    os.makedirs("migrations/versions", exist_ok=True)
    with open("alembic.ini", "w") as f:
        f.write(ALEMBIC_INI)
    with open("migrations/env.py", "w") as f:
        f.write(ALEMBIC_ENV)
    with open("migrations/__init__.py", "w") as f:
        f.write("")
    with open("migrations/script.py.mako", "w") as f:
        f.write('"""${message}\nRevision ID: ${up_revision}\nRevises: ${down_revision}\n"""\nfrom alembic import op\nimport sqlalchemy as sa\n${imports if imports else ""}\nrevision = ${repr(up_revision)}\ndown_revision = ${repr(down_revision)}\nbranch_labels = ${repr(branch_labels)}\ndepends_on = ${repr(depends_on)}\n\ndef upgrade():\n    ${upgrades if upgrades else "pass"}\n\ndef downgrade():\n    ${downgrades if downgrades else "pass"}\n')
    logger.info("✅ Alembic files created")
    logger.info("   Now run: alembic revision --autogenerate -m 'initial'")
    logger.info("   Then:    alembic upgrade head")


def migrate_data(sqlite_url, postgres_url):
    from sqlalchemy import create_engine, text, inspect
    from sqlalchemy.orm import sessionmaker

    logger.info("🔄 Starting data migration: SQLite → PostgreSQL")

    try:
        sqlite_engine = create_engine(sqlite_url)
        pg_engine = create_engine(postgres_url)
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return

    sqlite_session = sessionmaker(bind=sqlite_engine)()
    pg_session = sessionmaker(bind=pg_engine)()

    default_tenant_id = str(uuid.uuid4())
    logger.info(f"Creating default tenant: {default_tenant_id}")

    try:
        pg_session.execute(text("""
            INSERT INTO tenants (id, name, slug, status, plan, admin_email, locale)
            VALUES (:id, :name, :slug, 'active', 'enterprise', :email, 'ar')
            ON CONFLICT DO NOTHING
        """), {"id": default_tenant_id, "name": "المستشفى الرئيسي", "slug": "main-hospital", "email": "admin@main-hospital.local"})
        pg_session.commit()
    except Exception as e:
        logger.error(f"Failed to create default tenant: {e}")
        pg_session.rollback()
        return

    inspector = inspect(sqlite_engine)
    pg_inspector = inspect(pg_engine)
    tables = inspector.get_table_names()
    pg_tables = pg_inspector.get_table_names()

    logger.info(f"SQLite tables found: {tables}")

    TABLE_MAP = {
        "patients": {"extra_cols": {"tenant_id": default_tenant_id}},
        "appointments": {"extra_cols": {"tenant_id": default_tenant_id}},
    }

    for sqlite_table in tables:
        if sqlite_table.startswith("_"):
            continue

        config = TABLE_MAP.get(sqlite_table, {})
        pg_table = config.get("pg_table", sqlite_table)
        extra_cols = config.get("extra_cols", {})

        if pg_table not in pg_tables:
            logger.warning(f"⚠️  No PG table for '{sqlite_table}', skipping")
            continue

        rows = sqlite_session.execute(text(f"SELECT * FROM {sqlite_table}")).fetchall()
        if not rows:
            logger.info(f"  {sqlite_table}: empty")
            continue

        logger.info(f"  Migrating {sqlite_table}: {len(rows)} rows")

        sqlite_cols = [col["name"] for col in inspector.get_columns(sqlite_table)]
        pg_cols = {col["name"] for col in pg_inspector.get_columns(pg_table)}

        success = 0
        for row in rows:
            row_dict = dict(zip(sqlite_cols, row))
            row_dict = {k: v for k, v in row_dict.items() if k in pg_cols}
            row_dict.update(extra_cols)

            if "id" not in row_dict or not row_dict["id"]:
                row_dict["id"] = str(uuid.uuid4())

            try:
                cols_str = ", ".join(f'"{k}"' for k in row_dict.keys())
                vals_str = ", ".join(f":{k}" for k in row_dict.keys())
                pg_session.execute(text(f'INSERT INTO "{pg_table}" ({cols_str}) VALUES ({vals_str}) ON CONFLICT DO NOTHING'), row_dict)
                success += 1
            except Exception as e:
                pg_session.rollback()
                logger.error(f"    Row error: {e}")

        pg_session.commit()
        logger.info(f"  ✅ {sqlite_table}: {success} migrated")


def apply_rls(postgres_url):
    from sqlalchemy import create_engine, text
    logger.info("🔒 Applying Row Level Security...")
    engine = create_engine(postgres_url)

    statements = [
        "ALTER TABLE patients ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE users ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE encounters ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE vitals ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE lab_orders ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE lab_results ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE radiology_orders ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE medication_orders ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE clinical_ai_analyses ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE appointments ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE departments ENABLE ROW LEVEL SECURITY",
        "ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY",
        "CREATE POLICY tenant_isolation_patients ON patients USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_users ON users USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_encounters ON encounters USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_vitals ON vitals USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_lab_orders ON lab_orders USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_lab_results ON lab_results USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_radiology ON radiology_orders USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_medications ON medication_orders USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_ai ON clinical_ai_analyses USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_appointments ON appointments USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_departments ON departments USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
        "CREATE POLICY tenant_isolation_audit ON audit_logs USING (tenant_id = current_setting('app.current_tenant_id')::uuid)",
    ]

    with engine.connect() as conn:
        for stmt in statements:
            try:
                conn.execute(text(stmt))
                conn.commit()
            except Exception as e:
                if "already exists" in str(e).lower():
                    logger.debug(f"Already exists: {stmt[:50]}")
                else:
                    logger.warning(f"RLS warning: {e}")

    logger.info("✅ RLS policies applied")


def seed_icd11(postgres_url):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    sys.path.insert(0, os.path.dirname(__file__))
    from app.services.icd11_service import ICD11Service

    logger.info("🏥 Seeding ICD-11 codes...")
    engine = create_engine(postgres_url)
    Session = sessionmaker(bind=engine)
    db = Session()

    service = ICD11Service(db)
    if service.is_seeded():
        from app.models import ICD11Code
        count = db.query(ICD11Code).count()
        logger.info(f"✅ Already seeded: {count} codes")
        db.close()
        return

    count = service.seed_from_bundled_json()
    if count == 0:
        logger.warning("⚠️  No bundled JSON found.")
        logger.warning("   Run first: python ../scripts/download_icd11.py --bundled-only")

    db.close()
    logger.info(f"✅ ICD-11 seeding done: {count} codes")


def verify(postgres_url):
    from sqlalchemy import create_engine, text
    logger.info("🔍 Verifying migration...")
    engine = create_engine(postgres_url)

    tables = ["tenants", "users", "patients", "departments", "encounters",
              "vitals", "lab_orders", "lab_results", "radiology_orders",
              "medication_orders", "clinical_ai_analyses", "appointments",
              "icd11_codes", "audit_logs"]

    with engine.connect() as conn:
        for table in tables:
            try:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                logger.info(f"  ✅ {table}: {count} rows")
            except Exception as e:
                logger.error(f"  ❌ {table}: {e}")

        rls = conn.execute(text("""
            SELECT tablename, rowsecurity FROM pg_tables
            WHERE schemaname = 'public' AND tablename IN ('patients', 'users', 'encounters')
        """)).fetchall()

        logger.info("\n  RLS Status:")
        for row in rls:
            icon = "✅" if row[1] else "❌"
            logger.info(f"    {icon} {row[0]}: {'ON' if row[1] else 'OFF'}")

    logger.info("\n✅ Verification complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migration Tool")
    parser.add_argument("--step", choices=["all", "alembic", "data", "rls", "icd11", "verify"], default="all")
    parser.add_argument("--sqlite", default=SQLITE_URL)
    parser.add_argument("--postgres", default=POSTGRES_URL)
    args = parser.parse_args()

    steps = {
        "alembic": lambda: setup_alembic(),
        "data": lambda: migrate_data(args.sqlite, args.postgres),
        "rls": lambda: apply_rls(args.postgres),
        "icd11": lambda: seed_icd11(args.postgres),
        "verify": lambda: verify(args.postgres),
    }

    if args.step == "all":
        for name, fn in steps.items():
            logger.info(f"\n{'='*40}\nSTEP: {name.upper()}\n{'='*40}")
            fn()
    else:
        steps[args.step]()
