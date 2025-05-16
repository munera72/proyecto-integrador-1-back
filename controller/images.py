from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from fastapi.responses import FileResponse
from service.images_service import process_images
from service.images_service import get_zip

router = APIRouter(prefix="/images", tags=["Images"])



@router.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        result = await process_images(files)
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