import zipfile
import os
from config import settings  # Assuming you have a config file with this constant


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


