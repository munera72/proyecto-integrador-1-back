import zipfile
import os

def create_image_zip(image_paths, output_zip_path):
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


target_path = 'C:\\Users\\emanu\\Documents\\UdeA\\Material de estudio\\Proyecto integrador I\\Código\\back\\Reports\\test'
image_paths = ['C:\\Users\\emanu\\Pictures\\Saved Pictures\\wallpaper1.jpeg']

create_image_zip(image_paths, target_path)