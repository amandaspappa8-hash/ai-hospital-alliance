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






@router.get("/ahos/db/memory")
async def db_memory():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medical_memory_records ORDER BY created_at DESC")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "memory_records": rows
    }


@router.get("/ahos/db/hospital-nodes")
async def db_hospital_nodes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hospital_nodes ORDER BY created_at DESC")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "hospital_nodes": rows
    }
