from typing import Protocol


class AuditLogsRepositoryContract(Protocol):
    """Read boundary for tenant-scoped canonical audit-log persistence.

    The contract intentionally exposes read access only.

    Audit writes, schema migration, legacy SQLite repair, and null-tenant
    provenance are outside this security slice.
    """

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
        limit: int = 50,
    ) -> list[dict]:
        ...
