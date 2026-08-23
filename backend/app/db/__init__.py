from backend.app.db.database import (
    Base,
    engine,
    SessionLocal,
    get_db
)

def create_tables():
    Base.metadata.create_all(bind=engine)

def health_check():
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return {"db": "ok"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
