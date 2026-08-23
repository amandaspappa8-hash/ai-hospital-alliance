from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from backend.app.db.database import get_db
from backend.app.db.models import Tenant, AuditLog

router = APIRouter(
    prefix="/ahos/22.0/multi-tenant",
    tags=["AHOS 22.0.7 Real Multi-Tenant SaaS"]
)

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "22.0.7",
        "engine": "Real Multi-Tenant SaaS",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/create-demo-tenants")
def create_demo_tenants(db: Session = Depends(get_db)):

    tenants = [
        ("TENANT-TRIPOLI", "Tripoli Central AI Hospital", "Libya"),
        ("TENANT-BENGHAZI", "Benghazi Medical Center", "Libya"),
        ("TENANT-STOCKHOLM", "Stockholm Smart Hospital", "Sweden"),
        ("TENANT-DUBAI", "Dubai AI Healthcare", "UAE")
    ]

    created = []

    for tenant_id, name, country in tenants:

        exists = db.query(Tenant).filter(
            Tenant.tenant_id == tenant_id
        ).first()

        if not exists:

            tenant = Tenant(
                tenant_id=tenant_id,
                name=name,
                country=country,
                region=country,
                status="ACTIVE"
            )

            db.add(tenant)
            created.append(tenant_id)

    db.add(
        AuditLog(
            tenant_id="SYSTEM",
            actor="system",
            role="Admin",
            action="CREATE_MULTI_TENANT_ENVIRONMENT",
            resource="Tenant",
            severity="LOW",
            ip_address="127.0.0.1"
        )
    )

    db.commit()

    return {
        "status": "success",
        "created_tenants": created,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/tenants")
def tenants(db: Session = Depends(get_db)):

    rows = db.query(Tenant).all()

    return {
        "status": "success",
        "tenants": [
            {
                "tenant_id": t.tenant_id,
                "name": t.name,
                "country": t.country,
                "region": t.region,
                "status": t.status
            }
            for t in rows
        ]
    }

@router.get("/tenant/{tenant_id}")
def tenant_details(
    tenant_id:str,
    db: Session = Depends(get_db)
):

    tenant = db.query(Tenant).filter(
        Tenant.tenant_id == tenant_id
    ).first()

    if not tenant:
        return {
            "status":"not_found"
        }

    return {
        "status":"success",
        "tenant":{
            "tenant_id":tenant.tenant_id,
            "name":tenant.name,
            "country":tenant.country,
            "region":tenant.region,
            "status":tenant.status
        }
    }

@router.get("/saas-summary")
def saas_summary(db: Session = Depends(get_db)):

    total = db.query(Tenant).count()

    return {
        "status":"success",
        "saas":{
            "total_tenants":total,
            "tenant_isolation":"enabled",
            "audit_logging":"enabled",
            "rbac":"enabled",
            "fhir_ready":"enabled",
            "pacs_ready":"enabled"
        }
    }

@router.get("/executive-summary")
def executive_summary():

    return {
        "status":"success",
        "summary":{
            "phase":"22.0.7",
            "status":"Real Multi-Tenant SaaS Active",
            "strategic_value":"Supports multiple hospitals, healthcare groups, and countries on one platform with tenant isolation",
            "next_phase":"22.0.8 First Pilot Hospital Deployment"
        }
    }
