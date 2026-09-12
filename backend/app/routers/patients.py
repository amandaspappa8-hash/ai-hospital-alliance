from datetime import date
from typing import Any, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .deps import get_current_user, rate_limit_middleware
from ..models import Gender, Patient
from ..repositories.registry import (
    get_patients_repository,
    get_patients_repository_mode,
)
from ..services.core.patients_service import PatientsService
from ..tenant_isolation import (
    TenantContext,
    TenantSession,
    audit,
    bearer_scheme,
    get_db,
    get_tenant_context,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
    dependencies=[
        Depends(get_current_user),
        Depends(rate_limit_middleware),
    ],
)


class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    mrn: Optional[str] = None
    phone: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[list] = []
    chronic_conditions: Optional[list] = []


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[list] = None
    chronic_conditions: Optional[list] = None


def _model_dict(model: BaseModel) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()

    return model.dict()


def _canonical_identity(
    payload: dict[str, Any],
) -> tuple[int, str]:
    principal = payload.get("sub")
    tenant_id = payload.get("tenant_id")

    try:
        principal_user_id = int(principal)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid canonical Patient principal",
        ) from exc

    tenant_id = str(tenant_id or "").strip()

    if principal_user_id <= 0 or not tenant_id:
        raise HTTPException(
            status_code=401,
            detail="Incomplete canonical Patient token claims",
        )

    return principal_user_id, tenant_id


async def _patient_runtime(
    request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    mode = get_patients_repository_mode()

    if mode == "legacy_db":
        ctx = await get_tenant_context(
            request=request,
            credentials=credentials,
            db=db,
        )

        return {
            "mode": mode,
            "db": db,
            "ctx": ctx,
            "tdb": TenantSession(
                db,
                ctx.tenant_id,
            ),
        }

    repository = get_patients_repository()
    service = PatientsService(repository)

    principal_user_id, tenant_id = _canonical_identity(
        current_user
    )

    return {
        "mode": mode,
        "service": service,
        "principal_user_id": principal_user_id,
        "tenant_id": tenant_id,
    }


def _request_ip(request: Request) -> str | None:
    if request.client is None:
        return None

    return request.client.host


@router.get("")
def get_patients(
    current_user: dict[str, Any] = Depends(get_current_user),
):
    mode = get_patients_repository_mode()

    if mode == "legacy_db":
        return [
            {
                "id": "P-1001",
                "mrn": "MRN-1001",
                "full_name": "Ahmed Ali",
                "name": "Ahmed Ali",
                "date_of_birth": "1980-01-01",
                "gender": "male",
                "phone": "+218910000001",
                "blood_type": "O+",
                "allergies": [],
                "chronic_conditions": ["Hypertension"],
                "status": "Critical",
                "condition": "ICU observation",
                "department": "ICU",
            },
            {
                "id": "P-1002",
                "mrn": "MRN-1002",
                "full_name": "Sara Omar",
                "name": "Sara Omar",
                "date_of_birth": "1992-05-12",
                "gender": "female",
                "phone": "+218910000002",
                "blood_type": "A+",
                "allergies": ["Penicillin"],
                "chronic_conditions": [],
                "status": "Active",
                "condition": "Radiology follow-up",
                "department": "Radiology",
            },
        ]

    principal_user_id, tenant_id = _canonical_identity(
        current_user
    )

    return PatientsService(
        get_patients_repository()
    ).list_patients(
        tenant_id,
        principal_user_id,
    )


@router.get("/{patient_id}")
def get_patient(
    patient_id: str,
    request: Request,
    runtime: dict[str, Any] = Depends(_patient_runtime),
):
    if runtime["mode"] == "legacy_db":
        tdb: TenantSession = runtime["tdb"]
        ctx: TenantContext = runtime["ctx"]
        db: Session = runtime["db"]

        p = tdb.get_or_404(
            Patient,
            uuid.UUID(patient_id),
            "Patient",
        )

        audit(
            db,
            ctx,
            "patient.view",
            "Patient",
            p.id,
            request=request,
        )
        tdb.commit()

        return {
            "id": str(p.id),
            "mrn": p.mrn,
            "full_name": p.full_name,
            "date_of_birth": (
                str(p.date_of_birth)
                if p.date_of_birth is not None
                else None
            ),
            "gender": (
                p.gender.value
                if p.gender
                else None
            ),
            "phone": p.phone,
            "blood_type": p.blood_type,
            "allergies": p.allergies or [],
            "chronic_conditions": (
                p.chronic_conditions or []
            ),
            "current_medications": (
                p.current_medications or []
            ),
            "insurance_provider": (
                p.insurance_provider
            ),
        }

    return runtime["service"].get_patient(
        patient_id,
        runtime["tenant_id"],
        runtime["principal_user_id"],
    )


@router.post("", response_model=None)
def create_patient(
    data: PatientCreate,
    request: Request,
    runtime: dict[str, Any] = Depends(_patient_runtime),
):
    if runtime["mode"] == "legacy_db":
        tdb: TenantSession = runtime["tdb"]
        ctx: TenantContext = runtime["ctx"]
        db: Session = runtime["db"]

        mrn = (
            data.mrn
            or f"MRN-{str(uuid.uuid4())[:8].upper()}"
        )

        existing = (
            tdb.query(Patient)
            .filter(Patient.mrn == mrn)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"MRN {mrn} already exists",
            )

        p = Patient(
            id=uuid.uuid4(),
            mrn=mrn,
            full_name=data.full_name,
            date_of_birth=data.date_of_birth,
            gender=Gender(data.gender.lower()),
            phone=data.phone,
            blood_type=data.blood_type,
            allergies=data.allergies or [],
            chronic_conditions=(
                data.chronic_conditions or []
            ),
        )

        tdb.add(p)
        tdb.commit()
        tdb.refresh(p)

        audit(
            db,
            ctx,
            "patient.create",
            "Patient",
            p.id,
            {"mrn": mrn},
            request=request,
        )

        tdb.commit()

        return {
            "id": str(p.id),
            "mrn": p.mrn,
            "full_name": p.full_name,
        }

    created = runtime["service"].create_patient(
        _model_dict(data),
        runtime["tenant_id"],
        runtime["principal_user_id"],
        _request_ip(request),
    )

    return {
        "id": created["id"],
        "mrn": created.get("mrn"),
        "full_name": created.get("full_name"),
    }


@router.put("/{patient_id}", response_model=None)
def update_patient(
    patient_id: str,
    data: PatientUpdate,
    request: Request,
    runtime: dict[str, Any] = Depends(_patient_runtime),
):
    if runtime["mode"] == "legacy_db":
        tdb: TenantSession = runtime["tdb"]
        ctx: TenantContext = runtime["ctx"]
        db: Session = runtime["db"]

        p = tdb.get_or_404(
            Patient,
            uuid.UUID(patient_id),
            "Patient",
        )

        changes = {}

        if data.full_name is not None:
            changes["full_name"] = data.full_name
            p.full_name = data.full_name

        if data.phone is not None:
            changes["phone"] = data.phone
            p.phone = data.phone

        if data.blood_type is not None:
            p.blood_type = data.blood_type

        if data.allergies is not None:
            p.allergies = data.allergies

        if data.chronic_conditions is not None:
            p.chronic_conditions = (
                data.chronic_conditions
            )

        tdb.commit()

        audit(
            db,
            ctx,
            "patient.update",
            "Patient",
            p.id,
            changes,
            request=request,
        )

        tdb.commit()

        return {
            "success": True,
            "id": str(p.id),
        }

    updated = runtime["service"].update_patient(
        patient_id,
        _model_dict(data),
        runtime["tenant_id"],
        runtime["principal_user_id"],
        _request_ip(request),
    )

    return {
        "success": True,
        "id": updated["id"],
    }


@router.delete("/{patient_id}", response_model=None)
def delete_patient(
    patient_id: str,
    request: Request,
    runtime: dict[str, Any] = Depends(_patient_runtime),
):
    if runtime["mode"] == "legacy_db":
        tdb: TenantSession = runtime["tdb"]
        ctx: TenantContext = runtime["ctx"]
        db: Session = runtime["db"]

        p = tdb.get_or_404(
            Patient,
            uuid.UUID(patient_id),
            "Patient",
        )

        audit(
            db,
            ctx,
            "patient.delete",
            "Patient",
            p.id,
            request=request,
        )

        tdb.delete(p)
        tdb.commit()

        return {
            "success": True,
        }

    runtime["service"].delete_patient(
        patient_id,
        runtime["tenant_id"],
        runtime["principal_user_id"],
        _request_ip(request),
    )

    return {
        "success": True,
    }
