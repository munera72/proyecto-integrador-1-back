
from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/")
async def upload_images(files: List[UploadFile] = File(...)):
    file_details = []
    for file in files:
        file_details.append({"filename": file.filename, "content_type": file.content_type})
    return {"uploaded_files": file_details}