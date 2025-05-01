from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
import os
from uuid import uuid4
from pathlib import Path

from utils.img_utils import create_image_zip  # assuming your function is in zipper.py

router = APIRouter(prefix="/images", tags=["Images"])

TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_images(files: List[UploadFile] = File(...)):
    saved_paths = []

    for file in files:
        # Generate a unique name to avoid collisions
        temp_filename = f"{uuid4()}_{file.filename}"
        temp_path = TEMP_DIR / temp_filename

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_paths.append(str(temp_path))

    # Create ZIP
    create_image_zip(saved_paths)

    # Optionally clean up temp files
    for path in saved_paths:
        os.remove(path)

    return {
        "message": f"{len(saved_paths)} image(s) uploaded and zipped successfully.",
        "zip_location": str(create_image_zip.__defaults__[0])  # default zip path
    }
