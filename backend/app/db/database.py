import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.observability.sqlalchemy_tracing import sqlalchemy_span

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aiha_dev.db")

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    with sqlalchemy_span("session"):

        db = SessionLocal()

        try:
            yield db

        finally:
            db.close()
