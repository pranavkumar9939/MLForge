from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from app.services.dataset_services import analyze_dataset

router = APIRouter(prefix="/upload", tags=["Upload"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_FOLDER = BASE_DIR/"uploads"

UPLOAD_FOLDER.mkdir(exist_ok=True)

@router.post("/")
async def upload_dataset(file: UploadFile = File(...)):

    file_path = UPLOAD_FOLDER / file.filename

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    analysis = analyze_dataset(file_path)

    return {
        "filename": file.filename,
        "message": "File Uploaded successfully",
        "analysis": analysis
    }