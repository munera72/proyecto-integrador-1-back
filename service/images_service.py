from datetime import datetime
from pathlib import Path
from config import settings
from uuid import uuid4
import shutil
import os
from utils.img_utils import create_image_zip, process_image
from utils.model_utils import predict_and_save_masks
from utils.img_utils import validate_and_prepare_image

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


async def process_images(files, processing_data=None):
    saved_paths = []
    processed_paths = []
    timestamp = datetime.now().strftime("Report %d-%m-%Y %H-%M-%S")

    set_progress("Iniciando", 10)

    for idx, file in enumerate(files):
        temp_filename = file.filename 
        temp_path = TEMP_DIR / temp_filename

        validate_and_prepare_image(file, temp_path)
    
        saved_paths.append(str(temp_path))

        progress = 10 + int((idx + 1) / len(files) * 40)
        set_progress("Cargando imágenes", progress)

    # Process images according to processing_data['methods']
    if processing_data and "methods" in processing_data:
        for idx, method_dict in enumerate(processing_data["methods"]):
            image_name = method_dict.get("image")
            method = method_dict.get("method")
            # Find the corresponding saved image path
            img_path = next((p for p in saved_paths if Path(p).name == image_name), None)
            if img_path:
                processed_path = TEMP_DIR / f"processed_{Path(img_path).name}"
                process_image(img_path, processed_path, method_dict)
                processed_paths.append(str(processed_path))
            else:
                # If image not found, skip or handle error as needed
                continue
            progress = 50 + int((idx + 1) / len(processing_data["methods"]) * 30)
            set_progress("Procesando imágenes", progress)
    else:
        processed_paths = saved_paths.copy()

    # Clean up temp files
    for path in saved_paths:
        if os.path.exists(path):
            os.remove(path)
    
    set_progress("Modelo creando predicciones",85)

    mask_paths = predict_and_save_masks(TEMP_DIR)

    set_progress("Modelo creo predicciones",90)

    output_dir = Path(DEFAULT_TARGET_PATH) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    output_zip_path = output_dir / "report.zip"

    processed_paths += mask_paths

    set_progress("Creando archivo ZIP", 95)
    create_image_zip(processed_paths, output_zip_path)

    # Clean up temp files
    for path in processed_paths:
        if os.path.exists(path):
            os.remove(path)

    set_progress("Finalizado", 100)

    return {
        "message": f"{len(processed_paths)} image(s) processed and saved succesfully.",
        "file_name": timestamp,
    }


def get_zip(timestamp: str):
    zip_path = Path(DEFAULT_TARGET_PATH) / timestamp / "report.zip"
    if not zip_path.exists():
        raise FileNotFoundError("ZIP file not found")
    return str(zip_path)
