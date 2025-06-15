import numpy as np
import pytest
from utils import processing_methods


@pytest.fixture
def sample_image():
    # Create a 100x100 RGB image with random colors
    return (np.random.rand(100, 100, 3) * 255).astype(np.uint8)


def test_apply_gaussian_noise(sample_image):
    result = processing_methods.apply_gaussian_noise(sample_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_apply_random_brightness_contrast(sample_image):
    result = processing_methods.apply_random_brightness_contrast(sample_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_apply_random_rotation(sample_image):
    result = processing_methods.apply_random_rotation(sample_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_apply_horizontal_flip(sample_image):
    result = processing_methods.apply_horizontal_flip(sample_image)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_apply_gaussian_filter(sample_image):
    result = processing_methods.apply_gaussian_filter(sample_image, sigma=2.0)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert result.dtype == np.uint8

    # Check pixel value difference (blur effect)
    assert not np.array_equal(sample_image, result)
