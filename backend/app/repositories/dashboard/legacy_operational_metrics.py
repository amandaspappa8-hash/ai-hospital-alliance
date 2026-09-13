from __future__ import annotations

from .subsystem_metrics import (
    _open_read_only,
    resolve_active_operational_sqlite_path,
)


class LegacyOperationalMetricsAdapter:
    """
    Read-only compatibility adapter.

    These values preserve exact legacy dashboard semantics. They are not
    reclassified as canonical PostgreSQL clinical authority.
    """

    @staticmethod
    def empty() -> dict:
        return {
            "available_doctors": 0,
            "critical_lab_results": 0,
            "low_stock_drugs": 0,
            "hospitals": 0,
        }

    def read(self) -> dict:
        path = (
            resolve_active_operational_sqlite_path()
        )

        if path is None:
            return self.empty()

        conn = _open_read_only(path)

        if conn is None:
            return self.empty()

        try:
            queries = {
                "available_doctors": """
                    SELECT COUNT(*) AS count
                    FROM ahos_users
                    WHERE lower(
                        coalesce(role,'')
                    ) IN (
                        'doctor',
                        'physician',
                        'radiologist'
                    )
                    AND coalesce(is_active,1)=1
                """,
                "critical_lab_results": """
                    SELECT COUNT(*) AS count
                    FROM lab_results
                    WHERE
                        lower(
                            coalesce(status,'')
                        ) IN (
                            'critical',
                            'high',
                            'abnormal'
                        )
                        OR
                        coalesce(critical,0)=1
                """,
                "low_stock_drugs": """
                    SELECT COUNT(*) AS count
                    FROM pharmacy_inventory
                    WHERE
                        coalesce(stock_qty,0)
                        <= coalesce(min_qty,0)
                """,
                "hospitals": """
                    SELECT COUNT(*) AS count
                    FROM ahos_hospitals
                """,
            }

            result = {}

            for key, sql in queries.items():
                row = conn.execute(
                    sql
                ).fetchone()

                result[key] = int(
                    row["count"] or 0
                )

            return result

        except Exception:
            return self.empty()

        finally:
            conn.close()
