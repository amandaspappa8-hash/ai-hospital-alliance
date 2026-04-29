import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:////home/mohammed-elfallah/ai-hospital-alliance/hospital_dev.db",
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

IS_SQLITE = "sqlite" in DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    **(
        {"check_same_thread": False}
        if IS_SQLITE
        else {
            "pool_size": 20,
            "max_overflow": 40,
            "pool_recycle": 3600,
            "pool_timeout": 30,
        }
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from . import models

    Base.metadata.create_all(bind=engine)
    print(f"[DB] Tables ready — {DATABASE_URL[:50]}...")


def health_check() -> dict:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok", "url": DATABASE_URL[:30] + "..."}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
