from __future__ import annotations

from pathlib import Path
import os
import sqlite3
from urllib.parse import urlparse


def resolve_active_operational_sqlite_path() -> Path | None:
    value = (
        os.getenv("AHOS_DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or "sqlite:///./ahos_local_runtime.db"
    )

    parsed = urlparse(value)

    if not parsed.scheme.startswith("sqlite"):
        return None

    if value.startswith("sqlite:///./"):
        return Path(
            value[len("sqlite:///./"):]
        ).resolve()

    if value.startswith("sqlite:///"):
        return Path(
            value[len("sqlite:///"):]
        ).resolve()

    return None


def _open_read_only(path: Path):
    if not path.is_file():
        return None

    uri = f"file:{path.resolve()}?mode=ro"

    conn = sqlite3.connect(
        uri,
        uri=True,
        timeout=5,
    )
    conn.row_factory = sqlite3.Row
    return conn


class PhysicianReviewMetricsAdapter:
    """Read-only adapter for AHOS 56.x physician review metrics."""

    def __init__(
        self,
        db_path: Path | None = None,
    ) -> None:
        self.db_path = db_path or Path(
            "backend/app/ahos_55_8/"
            "ahos_55_8_avatar_memory.db"
        )

    @staticmethod
    def empty() -> dict:
        return {
            "available": False,
            "total_reviews": 0,
            "pending_reviews": 0,
            "approved_reviews": 0,
            "rejected_reviews": 0,
            "needs_more_review": 0,
            "urgent_reviews": 0,
        }

    def read(self) -> dict:
        result = self.empty()

        conn = _open_read_only(
            self.db_path.resolve()
        )

        if conn is None:
            return result

        try:
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
                        WHEN lower(
                            coalesce(review_status,'')
                        )='pending'
                        THEN 1 ELSE 0
                        END
                    ) AS pending_reviews,
                    SUM(
                        CASE
                        WHEN lower(
                            coalesce(review_status,'')
                        )='approved'
                        THEN 1 ELSE 0
                        END
                    ) AS approved_reviews,
                    SUM(
                        CASE
                        WHEN lower(
                            coalesce(review_status,'')
                        )='rejected'
                        THEN 1 ELSE 0
                        END
                    ) AS rejected_reviews,
                    SUM(
                        CASE
                        WHEN lower(
                            coalesce(review_status,'')
                        )='needs_more_review'
                        THEN 1 ELSE 0
                        END
                    ) AS needs_more_review,
                    SUM(
                        CASE
                        WHEN lower(
                            coalesce(priority,'')
                        )='urgent'
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

        except Exception:
            return self.empty()

        finally:
            conn.close()

        return result


class PersistentEventMetricsAdapter:
    """Read-only adapter for the AIHA/AHOS persistent event database."""

    def __init__(
        self,
        db_path: Path | None = None,
    ) -> None:
        self.db_path = db_path or Path(
            "aiha_ahos.db"
        )

    @staticmethod
    def empty() -> dict:
        return {
            "available": False,
            "patient_states": 0,
            "decision_logs": 0,
            "bus_events": 0,
            "hospital_nodes": 0,
            "critical_decisions": 0,
            "high_priority_events": 0,
        }

    def read(self) -> dict:
        result = self.empty()

        conn = _open_read_only(
            self.db_path.resolve()
        )

        if conn is None:
            return result

        try:
            def count(sql: str) -> int:
                row = conn.execute(
                    sql
                ).fetchone()

                if row is None:
                    return 0

                try:
                    return int(
                        row["count"] or 0
                    )
                except Exception:
                    return int(
                        row[0] or 0
                    )

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
                        WHERE lower(
                            coalesce(decision_level,'')
                        )='critical'
                        """
                    ),
                    "high_priority_events": count(
                        """
                        SELECT COUNT(*) AS count
                        FROM bus_events
                        WHERE lower(
                            coalesce(priority,'')
                        ) IN ('high','critical')
                        """
                    ),
                }
            )

        except Exception:
            return self.empty()

        finally:
            conn.close()

        return result


class ClinicalSafetyMetricsAdapter:
    """Read-only compatibility adapter for persisted clinical alerts."""

    @staticmethod
    def empty() -> dict:
        return {
            "available": False,
            "active_alerts": 0,
            "critical_alerts": 0,
        }

    def read(self) -> dict:
        result = self.empty()

        path = (
            resolve_active_operational_sqlite_path()
        )

        if path is None:
            return result

        conn = _open_read_only(path)

        if conn is None:
            return result

        try:
            table = conn.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                  AND name='clinical_safety_alerts'
                """
            ).fetchone()

            if table is None:
                return result

            active = conn.execute(
                """
                SELECT COUNT(*) AS count
                FROM clinical_safety_alerts
                WHERE lower(coalesce(status,'')) IN (
                    'active',
                    'open',
                    'pending'
                )
                """
            ).fetchone()["count"]

            critical = conn.execute(
                """
                SELECT COUNT(*) AS count
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
            ).fetchone()["count"]

            return {
                "available": True,
                "active_alerts": int(
                    active or 0
                ),
                "critical_alerts": int(
                    critical or 0
                ),
            }

        except Exception:
            return self.empty()

        finally:
            conn.close()
