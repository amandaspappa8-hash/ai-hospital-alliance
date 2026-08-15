from datetime import datetime, timezone
from pathlib import Path
import os
import sqlite3

from fastapi import APIRouter
from sqlalchemy import create_engine, text


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Unified Dashboard"],
)


def get_database_url() -> str:
    """
    Canonical AHOS operational database.

    AHOS_DATABASE_URL has priority because the verified production
    dashboard runtime currently uses ahos_local_runtime.db.
    """
    return (
        os.getenv("AHOS_DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or "sqlite:///./ahos_local_runtime.db"
    )


engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
)


SAFETY_DB = Path(
    "backend/app/ahos_55_8/ahos_55_8_avatar_memory.db"
)


def safe_count(sql: str) -> int:
    """
    Read a persisted operational KPI.

    Missing/unavailable data returns zero.
    Synthetic fallback values are prohibited.
    """
    try:
        with engine.connect() as conn:
            value = conn.execute(text(sql)).scalar()
            return int(value or 0)

    except Exception as exc:
        print(
            "[AHOS Dashboard SQL] "
            f"{type(exc).__name__}: {exc}"
        )
        return 0


def get_safety_metrics() -> dict:
    """
    Read persisted AHOS 56.x physician-review metrics.

    Database is opened read-only.
    """
    result = {
        "available": False,
        "total_reviews": 0,
        "pending_reviews": 0,
        "approved_reviews": 0,
        "rejected_reviews": 0,
        "needs_more_review": 0,
        "urgent_reviews": 0,
    }

    if not SAFETY_DB.is_file():
        return result

    conn = None

    try:
        uri = f"file:{SAFETY_DB.resolve()}?mode=ro"

        conn = sqlite3.connect(
            uri,
            uri=True,
            timeout=5,
        )

        conn.row_factory = sqlite3.Row

        table = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
              AND name='physician_review_queue'
            """
        ).fetchone()

        if table is None:
            return result

        row = conn.execute(
            """
            SELECT
                COUNT(*) AS total_reviews,

                SUM(
                    CASE
                    WHEN lower(coalesce(review_status,''))='pending'
                    THEN 1 ELSE 0
                    END
                ) AS pending_reviews,

                SUM(
                    CASE
                    WHEN lower(coalesce(review_status,''))='approved'
                    THEN 1 ELSE 0
                    END
                ) AS approved_reviews,

                SUM(
                    CASE
                    WHEN lower(coalesce(review_status,''))='rejected'
                    THEN 1 ELSE 0
                    END
                ) AS rejected_reviews,

                SUM(
                    CASE
                    WHEN lower(coalesce(review_status,''))='needs_more_review'
                    THEN 1 ELSE 0
                    END
                ) AS needs_more_review,

                SUM(
                    CASE
                    WHEN lower(coalesce(priority,''))='urgent'
                    THEN 1 ELSE 0
                    END
                ) AS urgent_reviews

            FROM physician_review_queue
            """
        ).fetchone()

        result.update(
            {
                "available": True,
                "total_reviews": int(
                    row["total_reviews"] or 0
                ),
                "pending_reviews": int(
                    row["pending_reviews"] or 0
                ),
                "approved_reviews": int(
                    row["approved_reviews"] or 0
                ),
                "rejected_reviews": int(
                    row["rejected_reviews"] or 0
                ),
                "needs_more_review": int(
                    row["needs_more_review"] or 0
                ),
                "urgent_reviews": int(
                    row["urgent_reviews"] or 0
                ),
            }
        )

    except Exception as exc:
        print(
            "[AHOS Dashboard Safety] "
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        if conn is not None:
            conn.close()

    return result


def get_persistent_event_metrics() -> dict:
    """
    Read AHOS persistent event storage using its canonical
    database module.

    No test events are created here.
    """
    result = {
        "available": False,
        "patient_states": 0,
        "decision_logs": 0,
        "bus_events": 0,
        "hospital_nodes": 0,
        "critical_decisions": 0,
        "high_priority_events": 0,
    }

    conn = None

    try:
        from backend.app.database.ahos_db import get_connection

        conn = get_connection()
        cur = conn.cursor()

        def count(sql: str) -> int:
            cur.execute(sql)
            row = cur.fetchone()

            if row is None:
                return 0

            try:
                return int(row["count"] or 0)
            except Exception:
                return int(row[0] or 0)

        result.update(
            {
                "available": True,

                "patient_states": count(
                    """
                    SELECT COUNT(*) AS count
                    FROM patient_states
                    """
                ),

                "decision_logs": count(
                    """
                    SELECT COUNT(*) AS count
                    FROM decision_logs
                    """
                ),

                "bus_events": count(
                    """
                    SELECT COUNT(*) AS count
                    FROM bus_events
                    """
                ),

                "hospital_nodes": count(
                    """
                    SELECT COUNT(*) AS count
                    FROM hospital_nodes
                    """
                ),

                "critical_decisions": count(
                    """
                    SELECT COUNT(*) AS count
                    FROM decision_logs
                    WHERE lower(coalesce(decision_level,''))
                          = 'critical'
                    """
                ),

                "high_priority_events": count(
                    """
                    SELECT COUNT(*) AS count
                    FROM bus_events
                    WHERE lower(coalesce(priority,''))
                          IN ('high','critical')
                    """
                ),
            }
        )

    except Exception as exc:
        print(
            "[AHOS Dashboard Events] "
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        if conn is not None:
            conn.close()

    return result


@router.get("/overview")
async def overview():

    total_patients = safe_count(
        "SELECT COUNT(*) FROM patients"
    )

    available_doctors = safe_count(
        """
        SELECT COUNT(*)
        FROM ahos_users
        WHERE lower(coalesce(role,'')) IN (
            'doctor',
            'physician',
            'radiologist'
        )
        AND coalesce(is_active,1)=1
        """
    )

    active_alerts = safe_count(
        """
        SELECT COUNT(*)
        FROM clinical_safety_alerts
        WHERE lower(coalesce(status,'')) IN (
            'active',
            'open',
            'pending'
        )
        """
    )

    critical_alerts = safe_count(
        """
        SELECT COUNT(*)
        FROM clinical_safety_alerts
        WHERE
            lower(coalesce(alert_level,'')) IN (
                'critical',
                'high'
            )
            OR
            lower(coalesce(priority,'')) IN (
                'critical',
                'high'
            )
            OR
            coalesce(risk_score,0) >= 0.8
        """
    )

    radiology_studies = safe_count(
        "SELECT COUNT(*) FROM radiology_studies"
    )

    ultrasound_studies = safe_count(
        "SELECT COUNT(*) FROM ultrasound_studies"
    )

    critical_lab_results = safe_count(
        """
        SELECT COUNT(*)
        FROM lab_results
        WHERE
            lower(coalesce(status,'')) IN (
                'critical',
                'high',
                'abnormal'
            )
            OR
            coalesce(critical,0)=1
        """
    )

    low_stock_drugs = safe_count(
        """
        SELECT COUNT(*)
        FROM pharmacy_inventory
        WHERE coalesce(stock_qty,0)
              <= coalesce(min_qty,0)
        """
    )

    hospitals = safe_count(
        "SELECT COUNT(*) FROM ahos_hospitals"
    )

    safety = get_safety_metrics()
    events = get_persistent_event_metrics()

    return {
        "source": "ahos_canonical_persisted_sources",

        "real_data": True,

        "synthetic_metrics": False,

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "kpis": {
            "total_patients": total_patients,
            "available_doctors": available_doctors,
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
            "radiology_studies": radiology_studies,
            "ultrasound_studies": ultrasound_studies,
            "critical_lab_results": critical_lab_results,
            "low_stock_drugs": low_stock_drugs,
            "hospitals": hospitals,

            "physician_reviews":
                safety["total_reviews"],

            "pending_physician_reviews":
                safety["pending_reviews"],

            "urgent_physician_reviews":
                safety["urgent_reviews"],

            "patient_states":
                events["patient_states"],

            "decision_logs":
                events["decision_logs"],

            "bus_events":
                events["bus_events"],

            "critical_decisions":
                events["critical_decisions"],

            "high_priority_events":
                events["high_priority_events"],
        },

        "safety": {
            "source":
                "AHOS 56.x physician_review_queue",

            "available":
                safety["available"],

            "total_reviews":
                safety["total_reviews"],

            "pending_reviews":
                safety["pending_reviews"],

            "approved_reviews":
                safety["approved_reviews"],

            "rejected_reviews":
                safety["rejected_reviews"],

            "needs_more_review":
                safety["needs_more_review"],

            "urgent_reviews":
                safety["urgent_reviews"],
        },

        "persistent_events": {
            "source":
                "AHOS Persistent Events Database",

            **events,
        },

        "status": "dashboard_operational",
    }
