from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import shutil
import os
from uuid import uuid4
from pathlib import Path
from config import settings
from fastapi.responses import FileResponse
from utils.img_utils import create_image_zip

router = APIRouter(prefix="/images", tags=["Images"])


DEFAULT_TARGET_PATH = settings.DEFAULT_TARGET_PATH
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    saved_paths = []

    for file in files:
        # Generate a unique name to avoid collisions
        temp_filename = f"{uuid4()}_{file.filename}"
        temp_path = TEMP_DIR / temp_filename

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_paths.append(str(temp_path))

    create_image_zip(saved_paths)

    for path in saved_paths:
        os.remove(path)

    return {
        "message": f"{len(saved_paths)} image(s) uploaded and zipped successfully.",
        "zip_location": str(create_image_zip.__defaults__[0])  # default zip path
    }


@router.get("/download")
async def download_zip():
    if not os.path.exists(DEFAULT_TARGET_PATH):
        raise HTTPException(status_code=404, detail="ZIP file not found.")
    
    return FileResponse(
        path=DEFAULT_TARGET_PATH,
        media_type='application/zip',
        filename="images.zip"
    )