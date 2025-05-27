from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from fastapi.responses import FileResponse
from service.images_service import process_images
from service.images_service import get_zip
from service.images_service import get_progress
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from pydantic import BaseModel
import json

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/progress/")
async def check_progress():
    return get_progress()



@router.post("/upload/")
async def upload_images(
    processing_data: str = Form(...),
    files: List[UploadFile] = File(...)
):
    try:
        # Parse the JSON string to a Python dict
        processing_data_dict = json.loads(processing_data)

        print(f"Processing data: {(processing_data_dict)}")
        result = await process_images(files, processing_data_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{report_name}")
async def download_zip(report_name: str):
    try:
        zip_path = get_zip(report_name)
        return FileResponse(
            path=zip_path,
            media_type='application/zip',
            filename="images.zip"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="ZIP file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))