from fastapi import APIRouter

router = APIRouter(
    prefix="/ahos/28.6",
    tags=["AHOS 28.6 Kubernetes & Cloud Native Platform"]
)

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 28.6",
        "module": "Kubernetes & Cloud Native Platform",
        "cloud_native": "enabled"
    }

@router.get("/stack")
async def stack():
    return {
        "backend": "kubernetes-ready",
        "postgresql": "kubernetes-ready",
        "keycloak": "kubernetes-ready",
        "orthanc": "kubernetes-ready",
        "ohif": "kubernetes-ready"
    }

@router.get("/architecture")
async def architecture():
    return {
        "namespace": "aiha",
        "deployments": ["backend", "postgres", "keycloak", "orthanc", "ohif"],
        "services": ["aiha-backend", "postgres", "keycloak", "orthanc", "ohif"],
        "next_phase": "AHOS 28.7 Monitoring, Prometheus & Grafana"
    }
