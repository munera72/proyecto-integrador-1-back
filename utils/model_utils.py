from tensorflow import keras
load_model = keras.models.load_model
from skimage.io import imread, imsave
import os
import numpy as np

def load_complete_model(model_path: str = 'D:\\Projects\\proyecto-integrador-1-back\\models\\unet_model128_epoch_100.keras'):
    try:
        model = load_model(model_path)
        print(f"Successfully loaded model from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def read_and_norm_images(images_array):
    new_images = []
    for img_path in images_array:
            image = imread(img_path)
            image_norm = (image / 255.0).astype(np.float32)
            new_images.append(image_norm)
    new_images_batch = np.array(new_images)
    return new_images_batch

def predict_with_model(model, input_batch):
    prediction = model.predict(input_batch)
    return prediction

def process_predictions(predictions):
    predicted_masks = np.argmax(predictions, axis=3)
    return predicted_masks

def convert_masks_to_images(predicted_masks, output_dir):
    color_map = {
        0: [0, 0, 0],     # Black
        1: [255, 0, 0],   # Red
        2: [0, 255, 0]    # Green
    }
    saved_paths = []
    for idx, mask in enumerate(predicted_masks):
        height, width = mask.shape
        color_image = np.zeros((height, width, 3), dtype=np.uint8)
        for class_index, color in color_map.items():
            color_image[mask == class_index] = color
        output_path = os.path.join(output_dir, f'mask_{idx + 1}.png')
        imsave(output_path, color_image)
        saved_paths.append(output_path)
    return saved_paths

def predict_and_save_masks(temp_folder):
    """
    Loads a model, processes all images in temp_folder, predicts masks, and saves them as PNGs.
    Args:
        temp_folder (str or Path): Folder containing images to process.
        model_path (str, optional): Path to the model file.
    Returns:
        List of saved mask file paths.
    """
    # Get all image files in the folder (you can filter by extension if needed)
    image_files = [os.path.join(temp_folder, f) for f in os.listdir(temp_folder)
                   if f.lower().endswith(('.png'))]

    if not image_files:
        print("No images found in the provided folder.")
        return []

    model = load_complete_model()
    images_batch = read_and_norm_images(image_files)
    predictions = predict_with_model(model, images_batch)
    predicted_masks = process_predictions(predictions)
    mask_paths = convert_masks_to_images(predicted_masks,temp_folder)
    return mask_paths