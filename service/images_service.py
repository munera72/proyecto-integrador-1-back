from pathlib import Path
from config import settings
from uuid import uuid4
import shutil
import os
from utils.img_utils import create_image_zip


DEFAULT_TARGET_PATH = settings.DEFAULT_TARGET_PATH
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

async def process_images(files):
    saved_paths = []

    #here we will process the images with the model, yet to implement
    # original_images = []
    # proccessed_images = []

    for file in files:
            temp_filename = f"{uuid4()}_{file.filename}"
            temp_path = TEMP_DIR / temp_filename
            #originals_path = TEMP_DIR / "original" / temp_filename
            #proccessed_path = TEMP_DIR / "proccessed" / temp_filename

            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            saved_paths.append(str(temp_path))

    create_image_zip(saved_paths)

    for path in saved_paths:
        os.remove(path)

    return {
        "message": f"{len(saved_paths)} image(s) processed and saved succesfully.",
    }


def get_zip():
    zip_path = Path(DEFAULT_TARGET_PATH)
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found")
    return str(zip_path)