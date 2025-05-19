from datetime import datetime
from pathlib import Path
from config import settings
from uuid import uuid4
import shutil
import os
from utils.img_utils import create_image_zip

# Variables internas para seguimiento del progreso
progress_status = {
    "status": "Esperando",
    "progress": 0
}

def set_progress(status: str, progress: int):
    progress_status["status"] = status
    progress_status["progress"] = progress

def get_progress():
    return progress_status


DEFAULT_TARGET_PATH = settings.DEFAULT_TARGET_PATH
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)


async def process_images(files):
    saved_paths = []
    timestamp = datetime.now().strftime("Report %d-%m-%Y %H-%M-%S")

    set_progress("Iniciando", 10)

    for idx, file in enumerate(files):
        temp_filename = f"{uuid4()}_{file.filename}"
        temp_path = TEMP_DIR / temp_filename

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_paths.append(str(temp_path))

        progress = 10 + int((idx + 1) / len(files) * 60)
        set_progress("Cargando imágenes", progress)

    output_dir = Path(DEFAULT_TARGET_PATH) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    output_zip_path = output_dir / "report.zip"

    set_progress("Creando archivo ZIP", 80)
    create_image_zip(saved_paths, output_zip_path)

    for path in saved_paths:
        os.remove(path)

    set_progress("Finalizado", 90)

    return {
        "message": f"{len(saved_paths)} image(s) processed and saved succesfully.",
        "file_name": timestamp,
    }


def get_zip(timestamp: str):
    zip_path = Path(DEFAULT_TARGET_PATH) / timestamp / "report.zip"
    if not zip_path.exists():
        raise FileNotFoundError("ZIP file not found")
    return str(zip_path)
