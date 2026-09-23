from __future__ import annotations

from typing import Any, Protocol, Sequence


class CanonicalSaaSRegistrationRepositoryContract(Protocol):
    """Canonical persistence boundary for POST /saas/register."""

    def slug_exists(
        self,
        *,
        slug: str,
        connection: Any,
    ) -> bool:
        ...

    def admin_email_exists(
        self,
        *,
        admin_email: str,
        connection: Any,
    ) -> bool:
        ...

    def tenant_id_exists(
        self,
        *,
        tenant_id: str,
        connection: Any,
    ) -> bool:
        ...

    def hospital_id_exists(
        self,
        *,
        hospital_id: str,
        connection: Any,
    ) -> bool:
        ...

    def department_code_exists(
        self,
        *,
        department_code: str,
        connection: Any,
    ) -> bool:
        ...

    def username_exists(
        self,
        *,
        username: str,
        connection: Any,
    ) -> bool:
        ...

    def create_registration_records(
        self,
        *,
        tenant_id: str,
        tenant_name: str,
        slug: str,
        plan: str,
        admin_email: str,
        admin_name: str,
        country: str,
        phone: str,
        api_key: str,
        trial_ends_at: Any | None,
        hospital_name: str,
        hospital_address: str,
        hospital_phone: str,
        departments: Sequence[tuple[str, str]],
        admin_username: str,
        admin_password_hash: str,
        admin_display_name: str,
        admin_role: str,
        connection: Any,
    ) -> dict[str, Any]:
        ...
