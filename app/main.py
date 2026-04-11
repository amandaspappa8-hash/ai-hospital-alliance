from fastapi import FastAPI
from app.api.clinical_route import router as clinical_route_router

app = FastAPI(
    title="AI Hospital Assistant API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "AI Hospital API running"}

# include AI Clinical Workflow router
app.include_router(clinical_route_router)
