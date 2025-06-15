import numpy as np
import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
import os

from utils import model_utils


@pytest.fixture
def dummy_image():
    # Simulate a 256x256 RGB image with values in 0-255
    return (np.random.rand(256, 256, 3) * 255).astype(np.uint8)


@pytest.fixture
def dummy_mask():
    # Simulate a 256x256 predicted mask with class values 0, 1, or 2
    return np.random.randint(0, 3, size=(256, 256), dtype=np.uint8)


def test_read_and_norm_images(tmp_path, dummy_image):
    image_path = tmp_path / "img.png"
    from skimage.io import imsave
    imsave(image_path, dummy_image)

    result = model_utils.read_and_norm_images([str(image_path)])
    assert isinstance(result, np.ndarray)
    assert result.shape == (1, 256, 256, 3)
    assert result.dtype == np.float32
    assert result.max() <= 1.0


def test_process_predictions():
    # Simulate softmax outputs for 2 images, 3 classes
    predictions = np.random.rand(2, 256, 256, 3)
    result = model_utils.process_predictions(predictions)
    assert isinstance(result, np.ndarray)
    assert result.shape == (2, 256, 256)
    assert result.dtype == np.int64


@patch("utils.model_utils.imsave")
def test_convert_masks_to_images(mock_imsave, tmp_path, dummy_mask):
    masks = np.array([dummy_mask, dummy_mask])
    output_paths = model_utils.convert_masks_to_images(masks, str(tmp_path))

    assert len(output_paths) == 2
    for path in output_paths:
        assert Path(path).exists() or "mask_" in path

    assert mock_imsave.call_count == 2


@patch("utils.model_utils.load_model")
def test_load_complete_model_success(mock_load_model):
    mock_model = MagicMock()
    mock_load_model.return_value = mock_model

    result = model_utils.load_complete_model("mock_path.keras")
    assert result == mock_model
    mock_load_model.assert_called_once()


@patch("utils.model_utils.load_model", side_effect=Exception("Failed"))
def test_load_complete_model_failure(mock_load_model):
    result = model_utils.load_complete_model("mock_path.keras")
    assert result is None


def test_predict_with_model():
    dummy_input = np.random.rand(2, 256, 256, 3)

    mock_model = MagicMock()
    mock_output = np.random.rand(2, 256, 256, 3)
    mock_model.predict.return_value = mock_output

    result = model_utils.predict_with_model(mock_model, dummy_input)
    assert result.shape == mock_output.shape
    mock_model.predict.assert_called_once()


@patch("utils.model_utils.load_complete_model")
@patch("utils.model_utils.convert_masks_to_images")
@patch("utils.model_utils.predict_with_model")
@patch("utils.model_utils.read_and_norm_images")
def test_predict_and_save_masks(
    mock_read_and_norm,
    mock_predict,
    mock_convert,
    mock_load_model,
    tmp_path,
    dummy_mask
):
    # Arrange mocks
    dummy_image = (tmp_path / "img.png")
    dummy_image.write_bytes(np.random.rand(256, 256, 3).astype(np.uint8).tobytes())
    dummy_image_paths = [str(dummy_image)]
    
    mock_model = MagicMock()
    mock_load_model.return_value = mock_model
    mock_read_and_norm.return_value = np.random.rand(1, 256, 256, 3)
    mock_predict.return_value = np.random.rand(1, 256, 256, 3)
    mock_convert.return_value = [str(tmp_path / "mask_1.png")]

    # Act
    result = model_utils.predict_and_save_masks(tmp_path)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    mock_load_model.assert_called_once()
    mock_read_and_norm.assert_called_once()
    mock_predict.assert_called_once()
    mock_convert.assert_called_once()
