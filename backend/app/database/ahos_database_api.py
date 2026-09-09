from fastapi import APIRouter
from datetime import datetime
from backend.app.database.ahos_db import get_connection

router = APIRouter(tags=["AHOS Persistent Database"])


@router.get("/ahos/db/health")
async def ahos_db_health():
    return {
        "status": "online",
        "engine": "AHOS Persistent Medical Intelligence Database",
        "version": "10.0.1",
        "timestamp": datetime.utcnow().isoformat()
    }




@router.get("/ahos/db/tables")
async def ahos_db_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row["name"] for row in cur.fetchall()]

    result = {}

    for table in tables:
        cur.execute(f"SELECT COUNT(*) as count FROM {table}")
        result[table] = cur.fetchone()["count"]

    conn.close()

    return {
        "status": "success",
        "tables": result
    }
