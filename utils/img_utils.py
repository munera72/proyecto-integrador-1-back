from fastapi import HTTPException
import zipfile
import os
from config import settings
from skimage.io import imread, imsave
from PIL import Image
from utils.processing_methods import (
    apply_gaussian_noise,
    apply_random_brightness_contrast,
    apply_random_rotation,
    apply_horizontal_flip,
    apply_gaussian_filter
)

MAX_SIZE_MB = 10
TARGET_SIZE = (256, 256)

def validate_and_prepare_image(upload_file, save_path):
    """
    Valida el tamaño, formato y dimensiones de la imagen, y la guarda como PNG 256x256 si es necesario.
    """

    upload_file.file.seek(0, 2) 
    size_mb = upload_file.file.tell() / (1024 * 1024)
    upload_file.file.seek(0)
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"{upload_file.filename} supera los 10MB permitidos.")
    try:
        image = Image.open(upload_file.file)
    except Exception:
        raise HTTPException(status_code=400, detail=f"No se pudo abrir {upload_file.filename} como imagen.")

    image = image.convert("RGB")

    if image.size != TARGET_SIZE:
        #print(f" Redimensionando {upload_file.filename} de {image.size} a {TARGET_SIZE}")
        image = image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

    image.save(save_path, format="PNG")

def create_image_zip(image_paths, output_zip_path = settings.DEFAULT_TARGET_PATH):

    """
    Creates a .zip file containing the images specified in the image_paths list.

    :param image_paths: List of paths to the image files to include in the .zip file.
    :param output_zip_path: Path where the .zip file will be created.
    """
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for image_path in image_paths:
            if os.path.isfile(image_path):
                zipf.write(image_path, os.path.basename(image_path))
            else:
                print(f"Warning: {image_path} does not exist and will be skipped.")


def process_image(image_path, processed_path, processing_data):
    """
    Processes an image according to the specified processing method.
    """
    # Read the image
    image = imread(image_path)
    method = processing_data.get("method", "").lower()
    print(f"processing method: {method}")
    # Switch-like logic for processing methods
    if method == "gaussian_noise":
        processed_image = apply_gaussian_noise(image)
    elif method == "random_brightness_contrast":
        processed_image = apply_random_brightness_contrast(image)
    elif method == "random_rotation":
        processed_image = apply_random_rotation(image)
    elif method == "horizontal_flip":
        processed_image = apply_horizontal_flip(image)
    elif method == "gaussian_filter":
        sigma = processing_data.get("sigma", 1.0)
        processed_image = apply_gaussian_filter(image, sigma=sigma)
    else:
        # If no valid method is provided, just copy the image
        print(f"Unknown processing method '{method}'. Copying image without changes.")
        os.rename(image_path, processed_path)
        print(f"Processed {image_path} to {processed_path}")
        return 

    # Save the processed image
    imsave(processed_path, processed_image)
    print(f"Processed {image_path} to {processed_path}")
