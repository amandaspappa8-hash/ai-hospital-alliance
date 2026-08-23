from fastapi import APIRouter

router = APIRouter(prefix="/enterprise-rbac", tags=["Enterprise RBAC"])

ROLE_PERMISSIONS = {
    "Admin": ["dashboard", "patients", "pharmacy", "labs", "radiology", "nursing", "audit", "ai"],
    "Doctor": ["patients", "orders", "labs", "pharmacy", "audit", "ai"],
    "Nurse": ["patients", "nursing", "mar", "notifications"],
    "Pharmacist": ["pharmacy", "mar", "drug_interactions", "audit"],
    "Radiology": ["radiology", "orders", "reports"],
}

@router.get("/{role}")
def get_permissions(role: str):
    return {
        "role": role,
        "permissions": ROLE_PERMISSIONS.get(role, []),
    }
