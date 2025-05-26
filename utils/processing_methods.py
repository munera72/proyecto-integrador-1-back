#import matplotlib.pyplot as plt
import numpy as np

#from skimage.io import imread, imshow, imread_collection, concatenate_images

import albumentations as A
from skimage.filters import gaussian


# A.GaussNoise(p=probs[0]),  # Apply Gaussian noise with a certain probability
# A.RandomBrightnessContrast(p=probs[1]),  # Apply random brightness/contrast change
# A.Rotate(p=probs[2]),  # Apply random rotation with a certain probability
# A.HorizontalFlip(p=probs[3]),  # Apply random horizontal flip

def apply_gaussian_noise(image):
    filter = A.GaussNoise(vp=1.0)
    return filter(image=image)['image']


def apply_random_brightness_contrast(image):
    filter = A.RandomBrightnessContrast(p=1.0)
    return filter(image=image)['image']

def apply_random_rotation(image):
    filter = A.Rotate(limit=30, p=1.0)  # Rotate by up to 30 degrees
    return filter(image=image)['image']

def apply_horizontal_flip(image):
    filter = A.HorizontalFlip(p=1.0)  # Apply horizontal flip
    return filter(image=image)['image']


def apply_gaussian_filter(image, sigma=1.0):
    """
    Apply Gaussian filter to an image using scikit-image.

    Args:
    - image (np.ndarray): Input image (can be RGB or grayscale).
    - sigma (float): Standard deviation of the Gaussian filter.
                     Larger values result in stronger blur.

    Returns:
    - blurred_image (np.ndarray): The blurred image.
    """
    # Apply Gaussian filter
    blurred_image = gaussian(image, sigma=sigma)
    blurred_image_uint8 = (blurred_image * 255).astype(np.uint8)
    return blurred_image_uint8
