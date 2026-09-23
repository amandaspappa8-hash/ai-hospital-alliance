from __future__ import annotations

from typing import Any, Sequence

from sqlalchemy import text
from sqlalchemy.engine import Engine

from backend.app.repositories.contracts.saas_registration_repository import (
    CanonicalSaaSRegistrationRepositoryContract,
)


class PostgresCanonicalSaaSRegistrationRepository(
    CanonicalSaaSRegistrationRepositoryContract
):
    """Canonical PostgreSQL persistence for POST /saas/register."""

    def __init__(
        self,
        engine: Engine,
    ) -> None:
        self._engine = engine

    @property
    def engine(self) -> Engine:
        return self._engine

    @staticmethod
    def _nonblank(
        name: str,
        value: str,
    ) -> str:
        if (
            not isinstance(value, str)
            or not value.strip()
        ):
            raise ValueError(
                f"{name} must be a non-empty string"
            )

        return value

    @staticmethod
    def _exists(
        *,
        connection: Any,
        statement: Any,
        parameters: dict[str, Any],
    ) -> bool:
        return bool(
            connection.execute(
                statement,
                parameters,
            ).scalar_one()
        )

    def slug_exists(
        self,
        *,
        slug: str,
        connection: Any,
    ) -> bool:
        value = self._nonblank(
            "slug",
            slug,
        )

        return self._exists(
            connection=connection,
            statement=text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.tenants
                    WHERE slug = :slug
                )
                """
            ),
            parameters={
                "slug": value,
            },
        )

    def admin_email_exists(
        self,
        *,
        admin_email: str,
        connection: Any,
    ) -> bool:
        value = self._nonblank(
            "admin_email",
            admin_email,
        )

        return self._exists(
            connection=connection,
            statement=text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.tenants
                    WHERE admin_email = :admin_email
                )
                """
            ),
            parameters={
                "admin_email": value,
            },
        )

    def tenant_id_exists(
        self,
        *,
        tenant_id: str,
        connection: Any,
    ) -> bool:
        value = self._nonblank(
            "tenant_id",
            tenant_id,
        )

        return self._exists(
            connection=connection,
            statement=text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.tenants
                    WHERE id = :tenant_id
                )
                """
            ),
            parameters={
                "tenant_id": value,
            },
        )

    def hospital_id_exists(
        self,
        *,
        hospital_id: str,
        connection: Any,
    ) -> bool:
        value = self._nonblank(
            "hospital_id",
            hospital_id,
        )

        return self._exists(
            connection=connection,
            statement=text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.hospitals
                    WHERE id = :hospital_id
                )
                """
            ),
            parameters={
                "hospital_id": value,
            },
        )

    def department_code_exists(
        self,
        *,
        department_code: str,
        connection: Any,
    ) -> bool:
        value = self._nonblank(
            "department_code",
            department_code,
        )

        return self._exists(
            connection=connection,
            statement=text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.departments
                    WHERE code = :department_code
                )
                """
            ),
            parameters={
                "department_code": value,
            },
        )

    def username_exists(
        self,
        *,
        username: str,
        connection: Any,
    ) -> bool:
        value = self._nonblank(
            "username",
            username,
        )

        return self._exists(
            connection=connection,
            statement=text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM public.users
                    WHERE username = :username
                )
                """
            ),
            parameters={
                "username": value,
            },
        )

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
        tenant = self._nonblank(
            "tenant_id",
            tenant_id,
        )

        tenant_name_value = self._nonblank(
            "tenant_name",
            tenant_name,
        )

        slug_value = self._nonblank(
            "slug",
            slug,
        )

        plan_value = self._nonblank(
            "plan",
            plan,
        )

        email_value = self._nonblank(
            "admin_email",
            admin_email,
        )

        api_key_value = self._nonblank(
            "api_key",
            api_key,
        )

        username_value = self._nonblank(
            "admin_username",
            admin_username,
        )

        password_hash_value = self._nonblank(
            "admin_password_hash",
            admin_password_hash,
        )

        role_value = self._nonblank(
            "admin_role",
            admin_role,
        )

        department_values = list(
            departments
        )

        if not department_values:
            raise ValueError(
                "departments must contain at least one department"
            )

        normalized_departments: list[
            tuple[str, str]
        ] = []

        for name, code in department_values:
            normalized_departments.append(
                (
                    self._nonblank(
                        "department_name",
                        name,
                    ),
                    self._nonblank(
                        "department_code",
                        code,
                    ),
                )
            )

        tenant_row = (
            connection.execute(
                text(
                    """
                    INSERT INTO public.tenants (
                        id,
                        name,
                        slug,
                        plan,
                        admin_email,
                        admin_name,
                        country,
                        phone,
                        api_key,
                        is_active,
                        is_verified,
                        trial_ends_at,
                        plan_starts_at,
                        settings,
                        ai_calls_today,
                        ai_calls_reset_at,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :id,
                        :name,
                        :slug,
                        :plan,
                        :admin_email,
                        :admin_name,
                        :country,
                        :phone,
                        :api_key,
                        TRUE,
                        FALSE,
                        :trial_ends_at,
                        NOW(),
                        '{}'::json,
                        0,
                        NOW(),
                        NOW(),
                        NOW()
                    )
                    RETURNING
                        id,
                        slug,
                        api_key
                    """
                ),
                {
                    "id": tenant,
                    "name": tenant_name_value,
                    "slug": slug_value,
                    "plan": plan_value,
                    "admin_email": email_value,
                    "admin_name": admin_name,
                    "country": country,
                    "phone": phone,
                    "api_key": api_key_value,
                    "trial_ends_at": trial_ends_at,
                },
            )
            .mappings()
            .one()
        )

        hospital_row = (
            connection.execute(
                text(
                    """
                    INSERT INTO public.hospitals (
                        id,
                        name,
                        address,
                        phone,
                        created_at,
                        tenant_id
                    )
                    VALUES (
                        :id,
                        :name,
                        :address,
                        :phone,
                        NOW(),
                        :tenant_id
                    )
                    RETURNING
                        id,
                        tenant_id
                    """
                ),
                {
                    "id": tenant,
                    "name": self._nonblank(
                        "hospital_name",
                        hospital_name,
                    ),
                    "address": hospital_address,
                    "phone": hospital_phone,
                    "tenant_id": tenant,
                },
            )
            .mappings()
            .one()
        )

        department_ids: list[int] = []

        for name, code in normalized_departments:
            department_row = (
                connection.execute(
                    text(
                        """
                        INSERT INTO public.departments (
                            name,
                            code,
                            hospital_id
                        )
                        VALUES (
                            :name,
                            :code,
                            :hospital_id
                        )
                        RETURNING
                            id,
                            code,
                            hospital_id
                        """
                    ),
                    {
                        "name": name,
                        "code": code,
                        "hospital_id": tenant,
                    },
                )
                .mappings()
                .one()
            )

            department_ids.append(
                int(
                    department_row["id"]
                )
            )

        user_row = (
            connection.execute(
                text(
                    """
                    INSERT INTO public.users (
                        username,
                        password,
                        name,
                        role,
                        hospital_id,
                        is_active,
                        created_at
                    )
                    VALUES (
                        :username,
                        :password,
                        :name,
                        :role,
                        :hospital_id,
                        TRUE,
                        NOW()
                    )
                    RETURNING
                        id,
                        username,
                        hospital_id
                    """
                ),
                {
                    "username": username_value,
                    "password": password_hash_value,
                    "name": admin_display_name,
                    "role": role_value,
                    "hospital_id": tenant,
                },
            )
            .mappings()
            .one()
        )

        return {
            "tenant_id": tenant_row["id"],
            "hospital_id": hospital_row["id"],
            "department_ids": department_ids,
            "user_id": user_row["id"],
            "api_key": tenant_row["api_key"],
        }
