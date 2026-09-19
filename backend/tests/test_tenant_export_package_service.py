from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from backend.app.services.core.tenant_export_package_service import (
    TenantExportPackageService,
)


HEAD = "78d652da578900bfe054d0073bc0f5348180f204"
FIXED_TIME = "2026-09-17T20:30:00+00:00"


def _snapshot() -> dict:
    return {
        "format_version": 1,
        "tenant_id": "T-TEST",
        "hospital_ids": [
            "H-2",
            "H-1",
        ],
        "table_count": 2,
        "record_count": 3,
        "tables": {
            "users": [
                {
                    "id": 2,
                    "hospital_id": "H-2",
                    "name": "Beta",
                },
                {
                    "id": 1,
                    "hospital_id": "H-1",
                    "name": "Alpha",
                },
            ],
            "tenants": [
                {
                    "id": "T-TEST",
                    "name": "Tenant",
                },
            ],
        },
        "excluded_tables": [
            "tenant_identity_bridge",
            "alembic_version",
        ],
        "excluded_fields": {
            "users": [
                "password",
            ],
            "tenants": [
                "api_key",
            ],
        },
    }


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)):
        path.read_bytes()
        for path in sorted(
            root.rglob("*")
        )
        if path.is_file()
    }


def _sha256(data: bytes) -> str:
    return hashlib.sha256(
        data
    ).hexdigest()


def test_builds_expected_v1_layout(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    result = service.build_package(
        _snapshot(),
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    assert result["package_form"] == "deterministic-directory"

    assert {
        str(path.relative_to(target))
        for path in target.rglob("*")
        if path.is_file()
    } == {
        "checksums.sha256",
        "export_summary.json",
        "manifest.json",
        "tables/tenants.jsonl",
        "tables/users.jsonl",
    }

    assert not list(
        target.rglob("*.zip")
    )

    assert not list(
        target.rglob("*.tar")
    )


def test_jsonl_bytes_are_canonical_and_deterministic(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    service.build_package(
        _snapshot(),
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    users = (
        target
        / "tables"
        / "users.jsonl"
    ).read_bytes()

    assert users == (
        b'{"hospital_id":"H-1","id":1,"name":"Alpha"}\n'
        b'{"hospital_id":"H-2","id":2,"name":"Beta"}\n'
    )


def test_empty_table_is_zero_bytes(tmp_path):
    snapshot = _snapshot()
    snapshot["tables"]["users"] = []
    snapshot["record_count"] = 1

    service = TenantExportPackageService()

    target = tmp_path / "export"

    service.build_package(
        snapshot,
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    assert (
        target
        / "tables"
        / "users.jsonl"
    ).read_bytes() == b""


def test_checksums_cover_tables_only_in_lexicographic_order(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    service.build_package(
        _snapshot(),
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    checksum_lines = (
        target
        / "checksums.sha256"
    ).read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(checksum_lines) == 2

    paths = [
        line.split("  ", 1)[1]
        for line in checksum_lines
    ]

    assert paths == sorted(paths)

    assert paths == [
        "tables/tenants.jsonl",
        "tables/users.jsonl",
    ]

    assert all(
        "manifest.json" not in line
        and "export_summary.json" not in line
        for line in checksum_lines
    )

    for line in checksum_lines:
        digest, relative_path = line.split(
            "  ",
            1,
        )

        assert digest == _sha256(
            (
                target
                / relative_path
            ).read_bytes()
        )


def test_content_set_digest_is_sha256_of_checksums_file(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    result = service.build_package(
        _snapshot(),
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    checksums = (
        target
        / "checksums.sha256"
    ).read_bytes()

    expected = _sha256(
        checksums
    )

    assert result[
        "content_set_sha256"
    ] == expected

    summary = json.loads(
        (
            target
            / "export_summary.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    manifest = json.loads(
        (
            target
            / "manifest.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert summary[
        "content_set_sha256"
    ] == expected

    assert manifest[
        "content_set_sha256"
    ] == expected


def test_manifest_summary_digest_has_no_self_reference(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    result = service.build_package(
        _snapshot(),
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    summary_bytes = (
        target
        / "export_summary.json"
    ).read_bytes()

    manifest_bytes = (
        target
        / "manifest.json"
    ).read_bytes()

    manifest = json.loads(
        manifest_bytes.decode(
            "utf-8"
        )
    )

    assert manifest[
        "export_summary_sha256"
    ] == _sha256(
        summary_bytes
    )

    assert (
        "manifest_sha256"
        not in manifest
    )

    assert (
        "package_sha256"
        not in manifest
    )

    assert result[
        "manifest_sha256"
    ] == _sha256(
        manifest_bytes
    )


def test_fixed_clock_build_is_byte_reproducible(tmp_path):
    service = TenantExportPackageService()

    first = tmp_path / "first"
    second = tmp_path / "second"

    service.build_package(
        _snapshot(),
        first,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    service.build_package(
        _snapshot(),
        second,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    assert _tree_bytes(
        first
    ) == _tree_bytes(
        second
    )


def test_different_clock_changes_manifest_only(tmp_path):
    service = TenantExportPackageService()

    first = tmp_path / "first"
    second = tmp_path / "second"

    service.build_package(
        _snapshot(),
        first,
        generated_at_utc="2026-09-17T20:30:00+00:00",
        source_git_head=HEAD,
    )

    service.build_package(
        _snapshot(),
        second,
        generated_at_utc="2026-09-17T20:31:00+00:00",
        source_git_head=HEAD,
    )

    first_files = _tree_bytes(
        first
    )

    second_files = _tree_bytes(
        second
    )

    assert (
        first_files.keys()
        == second_files.keys()
    )

    changed = {
        path
        for path in first_files
        if first_files[path]
        != second_files[path]
    }

    assert changed == {
        "manifest.json",
    }


def test_rejects_nonempty_target(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"
    target.mkdir()

    (
        target
        / "existing.txt"
    ).write_text(
        "do-not-overwrite",
        encoding="utf-8",
    )

    with pytest.raises(
        FileExistsError
    ):
        service.build_package(
            _snapshot(),
            target,
            generated_at_utc=FIXED_TIME,
            source_git_head=HEAD,
        )

    assert (
        target
        / "existing.txt"
    ).read_text(
        encoding="utf-8"
    ) == "do-not-overwrite"


def test_rejects_path_traversal_table_name(tmp_path):
    snapshot = _snapshot()

    snapshot["tables"] = {
        "../escape": [],
    }

    snapshot["table_count"] = 1
    snapshot["record_count"] = 0

    service = TenantExportPackageService()

    target = tmp_path / "export"

    with pytest.raises(
        ValueError,
        match="unsafe export table name",
    ):
        service.build_package(
            snapshot,
            target,
            generated_at_utc=FIXED_TIME,
            source_git_head=HEAD,
        )

    assert not target.exists()


def test_rejects_secret_field_reaching_package_layer(tmp_path):
    snapshot = _snapshot()

    snapshot["tables"]["users"][0][
        "password"
    ] = "SHOULD_NEVER_REACH_PACKAGE"

    service = TenantExportPackageService()

    target = tmp_path / "export"

    with pytest.raises(
        ValueError,
        match="secret field reached package layer",
    ):
        service.build_package(
            snapshot,
            target,
            generated_at_utc=FIXED_TIME,
            source_git_head=HEAD,
        )

    assert not target.exists()


def test_manifest_contains_policy_names_but_no_secret_values(tmp_path):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    service.build_package(
        _snapshot(),
        target,
        generated_at_utc=FIXED_TIME,
        source_git_head=HEAD,
    )

    manifest_text = (
        target
        / "manifest.json"
    ).read_text(
        encoding="utf-8"
    )

    assert '"password"' in manifest_text
    assert '"api_key"' in manifest_text

    assert (
        "SHOULD_NEVER_REACH_PACKAGE"
        not in manifest_text
    )


def test_failure_cleans_partial_build(tmp_path, monkeypatch):
    service = TenantExportPackageService()

    target = tmp_path / "export"

    original = service._write_bytes

    calls = {
        "count": 0,
    }

    def failing_write(
        package_root,
        relative_path,
        data,
    ):
        calls["count"] += 1

        if relative_path == "checksums.sha256":
            raise RuntimeError(
                "simulated package write failure"
            )

        return original(
            package_root,
            relative_path,
            data,
        )

    monkeypatch.setattr(
        service,
        "_write_bytes",
        failing_write,
    )

    with pytest.raises(
        RuntimeError,
        match="simulated package write failure",
    ):
        service.build_package(
            _snapshot(),
            target,
            generated_at_utc=FIXED_TIME,
            source_git_head=HEAD,
        )

    assert calls["count"] >= 2
    assert not target.exists()

    leftovers = [
        path
        for path in tmp_path.iterdir()
        if ".export.build-" in path.name
    ]

    assert leftovers == []


def test_source_contains_no_database_or_http_surface():
    source_path = Path(
        "backend/app/services/core/"
        "tenant_export_package_service.py"
    )

    source = source_path.read_text(
        encoding="utf-8"
    )

    assert "sqlalchemy" not in source.lower()
    assert ".execute(" not in source
    assert ".commit(" not in source

    assert "@app." not in source
    assert "@router." not in source

    assert "zipfile" not in source
    assert "tarfile" not in source



def test_package_rejects_nonportable_refresh_tokens():
    from backend.app.services.core.tenant_export_package_service import (
        TenantExportPackageService,
    )

    snapshot = {
        "tenant_id": "TEN-1",
        "hospital_ids": [],
        "tables": {
            "refresh_tokens": [],
        },
        "table_count": 1,
        "record_count": 0,
        "excluded_tables": [],
        "excluded_fields": {},
    }

    try:
        TenantExportPackageService._validate_snapshot(
            snapshot
        )
    except ValueError as exc:
        assert (
            "non-portable authentication security state table: "
            "refresh_tokens"
            in str(exc)
        )
    else:
        raise AssertionError(
            "package accepted non-portable refresh_tokens"
        )
