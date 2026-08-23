from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from backend.app.ai_ultrasound.engine import analyze_ultrasound

router = APIRouter(prefix="/ai-ultrasound", tags=["AI Ultrasound"])

UPLOAD_DIR = Path("app/uploads")

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_ultrasound(str(file_path))

    return result
