from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from backend.app.repositories.postgres.tenant_export_repository import (
    PostgresTenantExportRepository,
)


class TenantExportPackageService:
    """Build deterministic internal tenant-export package directories.

    This service operates only on an already-authorized, already-sanitized
    tenant export snapshot. It does not query or mutate the database and does
    not expose an HTTP endpoint.

    Package v1 deliberately uses a directory rather than ZIP/TAR so archive
    metadata does not affect deterministic package bytes.
    """

    FORMAT_VERSION = 1
    PACKAGE_FORM = "deterministic-directory"

    _TABLE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    _SOURCE_SECRET_FIELDS = {
        "tenants": frozenset({"api_key"}),
        "users": frozenset({"password"}),
        "refresh_tokens": frozenset({"token_hash"}),
    }

    @staticmethod
    def _sha256_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _canonical_json_bytes(value: Any) -> bytes:
        return (
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
            + b"\n"
        )

    @staticmethod
    def _normalize_generated_at(value: datetime | str | None) -> str:
        if value is None:
            dt = datetime.now(timezone.utc)

        elif isinstance(value, datetime):
            dt = value

        elif isinstance(value, str):
            candidate = value.strip()

            if candidate.endswith("Z"):
                candidate = candidate[:-1] + "+00:00"

            try:
                dt = datetime.fromisoformat(candidate)
            except ValueError as exc:
                raise ValueError(
                    "generated_at_utc must be ISO-8601"
                ) from exc

        else:
            raise TypeError(
                "generated_at_utc must be datetime, str, or None"
            )

        if dt.tzinfo is None:
            raise ValueError(
                "generated_at_utc must be timezone-aware"
            )

        return (
            dt.astimezone(timezone.utc)
            .isoformat(timespec="microseconds")
            .replace("+00:00", "Z")
        )

    @staticmethod
    def _normalize_string_list(value: Any) -> list[str]:
        if value is None:
            return []

        if not isinstance(value, (list, tuple, set, frozenset)):
            raise TypeError(
                "expected list-like value"
            )

        return sorted(
            {
                str(item)
                for item in value
            }
        )

    @classmethod
    def _normalize_excluded_fields(
        cls,
        value: Any,
    ) -> dict[str, list[str]]:
        if value is None:
            return {}

        if not isinstance(value, Mapping):
            raise TypeError(
                "excluded_fields must be a mapping"
            )

        normalized: dict[str, list[str]] = {}

        for table, fields in value.items():
            table_name = str(table)

            cls._validate_table_name(
                table_name
            )

            normalized[table_name] = (
                cls._normalize_string_list(
                    fields
                )
            )

        return {
            key: normalized[key]
            for key in sorted(normalized)
        }

    @classmethod
    def _validate_table_name(
        cls,
        table: str,
    ) -> None:
        if not cls._TABLE_NAME_RE.fullmatch(table):
            raise ValueError(
                f"unsafe export table name: {table!r}"
            )

        if (
            table
            not in PostgresTenantExportRepository.TABLE_STRATEGIES
        ):
            raise ValueError(
                f"table is not in canonical export whitelist: {table}"
            )

    @classmethod
    def _validate_snapshot(
        cls,
        snapshot: Mapping[str, Any],
    ) -> tuple[
        str,
        list[str],
        dict[str, list[dict[str, Any]]],
        list[str],
        dict[str, list[str]],
    ]:
        if not isinstance(snapshot, Mapping):
            raise TypeError(
                "snapshot must be a mapping"
            )

        tenant_id = str(
            snapshot.get("tenant_id", "")
        ).strip()

        if not tenant_id:
            raise ValueError(
                "snapshot tenant_id is required"
            )

        hospital_ids = cls._normalize_string_list(
            snapshot.get("hospital_ids", [])
        )

        raw_tables = snapshot.get("tables")

        if not isinstance(raw_tables, Mapping):
            raise TypeError(
                "snapshot tables must be a mapping"
            )

        tables: dict[str, list[dict[str, Any]]] = {}

        for raw_name, raw_rows in raw_tables.items():
            table = str(raw_name)

            cls._validate_table_name(
                table
            )

            if not isinstance(raw_rows, list):
                raise TypeError(
                    f"table rows must be a list: {table}"
                )

            clean_rows: list[dict[str, Any]] = []

            forbidden = cls._SOURCE_SECRET_FIELDS.get(
                table,
                frozenset(),
            )

            for row in raw_rows:
                if not isinstance(row, Mapping):
                    raise TypeError(
                        f"export row must be a mapping: {table}"
                    )

                row_dict = dict(row)

                leaked = (
                    forbidden
                    & set(row_dict)
                )

                if leaked:
                    raise ValueError(
                        "secret field reached package layer: "
                        + table
                        + "."
                        + ",".join(
                            sorted(leaked)
                        )
                    )

                clean_rows.append(
                    row_dict
                )

            tables[table] = clean_rows

        tables = {
            key: tables[key]
            for key in sorted(tables)
        }

        expected_table_count = len(
            tables
        )

        snapshot_table_count = snapshot.get(
            "table_count",
            expected_table_count,
        )

        if int(snapshot_table_count) != expected_table_count:
            raise ValueError(
                "snapshot table_count does not match tables"
            )

        expected_record_count = sum(
            len(rows)
            for rows in tables.values()
        )

        snapshot_record_count = snapshot.get(
            "record_count",
            expected_record_count,
        )

        if int(snapshot_record_count) != expected_record_count:
            raise ValueError(
                "snapshot record_count does not match tables"
            )

        excluded_tables = (
            cls._normalize_string_list(
                snapshot.get(
                    "excluded_tables",
                    [],
                )
            )
        )

        excluded_fields = (
            cls._normalize_excluded_fields(
                snapshot.get(
                    "excluded_fields",
                    {},
                )
            )
        )

        return (
            tenant_id,
            hospital_ids,
            tables,
            excluded_tables,
            excluded_fields,
        )

    @staticmethod
    def _assert_safe_relative_path(
        relative_path: str,
    ) -> None:
        path = Path(relative_path)

        if path.is_absolute():
            raise ValueError(
                "absolute package path is forbidden"
            )

        if ".." in path.parts:
            raise ValueError(
                "package path traversal is forbidden"
            )

    @classmethod
    def _write_bytes(
        cls,
        package_root: Path,
        relative_path: str,
        data: bytes,
    ) -> None:
        cls._assert_safe_relative_path(
            relative_path
        )

        destination = (
            package_root
            / relative_path
        )

        root_resolved = (
            package_root.resolve()
        )

        destination_resolved = (
            destination.resolve(
                strict=False
            )
        )

        try:
            destination_resolved.relative_to(
                root_resolved
            )
        except ValueError as exc:
            raise ValueError(
                "package path escaped output root"
            ) from exc

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.is_symlink():
            raise ValueError(
                "symlink output is forbidden"
            )

        with destination.open("xb") as stream:
            stream.write(data)

    @classmethod
    def _table_jsonl_bytes(
        cls,
        rows: list[dict[str, Any]],
    ) -> bytes:
        if not rows:
            return b""

        encoded = [
            cls._canonical_json_bytes(
                row
            )
            for row in rows
        ]

        # Snapshot rows should already be canonicalized, but sorting again
        # makes package determinism independent of caller list order.
        encoded.sort()

        if len(encoded) != len(set(encoded)):
            raise ValueError(
                "duplicate canonical rows reached package builder"
            )

        return b"".join(encoded)

    def build_package(
        self,
        snapshot: Mapping[str, Any],
        output_dir: str | os.PathLike[str],
        generated_at_utc: datetime | str | None = None,
        source_git_head: str | None = None,
    ) -> dict[str, Any]:
        (
            tenant_id,
            hospital_ids,
            tables,
            excluded_tables,
            excluded_fields,
        ) = self._validate_snapshot(
            snapshot
        )

        generated_at = (
            self._normalize_generated_at(
                generated_at_utc
            )
        )

        git_head = (
            source_git_head
            or snapshot.get(
                "source_git_head"
            )
        )

        if git_head is None:
            raise ValueError(
                "source_git_head is required"
            )

        git_head = str(
            git_head
        ).strip()

        if not re.fullmatch(
            r"[0-9a-f]{40}",
            git_head,
        ):
            raise ValueError(
                "source_git_head must be a 40-character lowercase Git SHA"
            )

        source_schema = str(
            snapshot.get(
                "source_schema",
                "public",
            )
        ).strip()

        if not source_schema:
            raise ValueError(
                "source_schema must not be blank"
            )

        target = Path(
            output_dir
        )

        if target.exists():
            if target.is_symlink():
                raise ValueError(
                    "symlink package target is forbidden"
                )

            if not target.is_dir():
                raise ValueError(
                    "package target exists and is not a directory"
                )

            if any(target.iterdir()):
                raise FileExistsError(
                    "package target must not already contain files"
                )

            target_preexisted_empty = True
        else:
            target_preexisted_empty = False

        parent = target.parent

        if (
            not parent.exists()
            or not parent.is_dir()
        ):
            raise ValueError(
                "package parent directory must already exist"
            )

        if parent.is_symlink():
            raise ValueError(
                "symlink package parent is forbidden"
            )

        temp_root = Path(
            tempfile.mkdtemp(
                prefix=f".{target.name}.build-",
                dir=str(parent),
            )
        )

        package_root = (
            temp_root
            / "package"
        )

        package_root.mkdir()

        try:
            table_entries: list[
                dict[str, Any]
            ] = []

            checksum_entries: list[
                tuple[str, str]
            ] = []

            total_records = 0

            for table in sorted(tables):
                rows = tables[table]

                relative_path = (
                    f"tables/{table}.jsonl"
                )

                data = self._table_jsonl_bytes(
                    rows
                )

                self._write_bytes(
                    package_root,
                    relative_path,
                    data,
                )

                digest = self._sha256_bytes(
                    data
                )

                checksum_entries.append(
                    (
                        relative_path,
                        digest,
                    )
                )

                table_entries.append(
                    {
                        "excluded_fields":
                        excluded_fields.get(
                            table,
                            [],
                        ),
                        "logical_path":
                        relative_path,
                        "ownership_strategy":
                        PostgresTenantExportRepository
                        .TABLE_STRATEGIES[
                            table
                        ],
                        "row_count":
                        len(rows),
                        "sha256":
                        digest,
                        "table":
                        table,
                    }
                )

                total_records += len(
                    rows
                )

            checksum_entries.sort(
                key=lambda item: item[0]
            )

            checksums_bytes = b"".join(
                (
                    digest
                    + "  "
                    + relative_path
                    + "\n"
                ).encode("utf-8")
                for relative_path, digest
                in checksum_entries
            )

            self._write_bytes(
                package_root,
                "checksums.sha256",
                checksums_bytes,
            )

            content_set_sha256 = (
                self._sha256_bytes(
                    checksums_bytes
                )
            )

            export_summary = {
                "content_set_sha256":
                content_set_sha256,

                "format_version":
                self.FORMAT_VERSION,

                "hospital_count":
                len(hospital_ids),

                "package_form":
                self.PACKAGE_FORM,

                "record_count":
                total_records,

                "table_count":
                len(tables),

                "tenant_id":
                tenant_id,
            }

            export_summary_bytes = (
                self._canonical_json_bytes(
                    export_summary
                )
            )

            self._write_bytes(
                package_root,
                "export_summary.json",
                export_summary_bytes,
            )

            export_summary_sha256 = (
                self._sha256_bytes(
                    export_summary_bytes
                )
            )

            manifest = {
                "content_set_sha256":
                content_set_sha256,

                "excluded_fields":
                excluded_fields,

                "excluded_tables":
                excluded_tables,

                "export_summary_sha256":
                export_summary_sha256,

                "format_version":
                self.FORMAT_VERSION,

                "generated_at_utc":
                generated_at,

                "hospital_ids":
                hospital_ids,

                "record_count":
                total_records,

                "source_git_head":
                git_head,

                "source_schema":
                source_schema,

                "table_count":
                len(tables),

                "tables":
                table_entries,

                "tenant_id":
                tenant_id,
            }

            manifest_bytes = (
                self._canonical_json_bytes(
                    manifest
                )
            )

            self._write_bytes(
                package_root,
                "manifest.json",
                manifest_bytes,
            )

            manifest_sha256 = (
                self._sha256_bytes(
                    manifest_bytes
                )
            )

            if target_preexisted_empty:
                target.rmdir()

            os.replace(
                package_root,
                target,
            )

            result = {
                "content_set_sha256":
                content_set_sha256,

                "export_summary_sha256":
                export_summary_sha256,

                "manifest_sha256":
                manifest_sha256,

                "package_form":
                self.PACKAGE_FORM,

                "path":
                str(target),

                "record_count":
                total_records,

                "table_count":
                len(tables),

                "tenant_id":
                tenant_id,
            }

            return result

        except Exception:
            if (
                target_preexisted_empty
                and not target.exists()
            ):
                target.mkdir()

            raise

        finally:
            shutil.rmtree(
                temp_root,
                ignore_errors=True,
            )
