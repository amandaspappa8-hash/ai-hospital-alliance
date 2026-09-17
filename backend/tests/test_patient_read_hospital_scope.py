import inspect

from backend.app.repositories.postgres.patients_repository import (
    PostgresPatientsRepository,
)


def test_patient_base_read_requires_tenant_and_hospital_scope():
    source = inspect.getsource(
        PostgresPatientsRepository._patient_select_sql
    )

    assert "h.tenant_id = :tenant_id" in source
    assert "p.hospital_id = :hospital_id" in source


def test_patient_list_binds_canonical_hospital_scope():
    source = inspect.getsource(
        PostgresPatientsRepository.list_all
    )

    assert source.count(
        '"tenant_id": scope["tenant_id"]'
    ) == 1

    assert source.count(
        '"hospital_id": scope["hospital_id"]'
    ) == 1


def test_patient_get_by_id_binds_canonical_hospital_scope():
    source = inspect.getsource(
        PostgresPatientsRepository.get_by_id
    )

    assert source.count(
        '"tenant_id": scope["tenant_id"]'
    ) == 1

    assert source.count(
        '"hospital_id": scope["hospital_id"]'
    ) == 1

    assert source.count(
        '"patient_id": patient_id'
    ) == 1


def test_patient_authorization_remains_hospital_tenant_scoped():
    source = inspect.getsource(
        PostgresPatientsRepository.authorize_patient_access
    )

    assert "p.id = :patient_id" in source
    assert "p.hospital_id = :hospital_id" in source
    assert "h.tenant_id = :tenant_id" in source


def test_patient_scope_resolver_derives_hospital_and_tenant():
    source = inspect.getsource(
        PostgresPatientsRepository._resolve_scope
    )

    assert "u.hospital_id" in source
    assert "h.tenant_id" in source
    assert '"hospital_id": str(hospital_id)' in source
    assert '"tenant_id": derived_tenant_id' in source
