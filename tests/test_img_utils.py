import io
import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from PIL import Image
from utils import img_utils


@pytest.fixture
def fake_upload_file():
    # Create a fake 256x256 RGB image in memory
    img_bytes = io.BytesIO()
    image = Image.new("RGB", (256, 256), color="white")
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    fake_file = MagicMock()
    fake_file.file = img_bytes
    fake_file.filename = "test_image.png"
    return fake_file


def test_validate_and_prepare_image_success(tmp_path, fake_upload_file):
    save_path = tmp_path / "resized_image.png"
    img_utils.validate_and_prepare_image(fake_upload_file, save_path)
    assert os.path.exists(save_path)


def test_validate_and_prepare_image_large_file(fake_upload_file):
    fake_upload_file.file.seek(0, 2)  # Go to end of stream
    fake_upload_file.file.tell = lambda: 11 * 1024 * 1024  # Simulate >10MB
    fake_upload_file.file.seek(0)

    with pytest.raises(HTTPException) as exc:
        img_utils.validate_and_prepare_image(fake_upload_file, "some_path.png")
    assert "supera los 10MB" in str(exc.value.detail)


def test_validate_and_prepare_image_invalid_file():
    bad_file = MagicMock()
    bad_file.file = io.BytesIO(b"not an image")
    bad_file.filename = "bad.img"

    with pytest.raises(HTTPException) as exc:
        img_utils.validate_and_prepare_image(bad_file, "output.png")
    assert "No se pudo abrir" in str(exc.value.detail)


@patch("utils.img_utils.zipfile.ZipFile")
def test_create_image_zip(mock_zipfile, tmp_path):
    fake_img = tmp_path / "img.png"
    fake_img.write_text("dummy data")

    zip_path = tmp_path / "output.zip"
    img_utils.create_image_zip([str(fake_img)], output_zip_path=str(zip_path))

    mock_zipfile.assert_called_once()
    assert zip_path.name == "output.zip"


@patch("utils.img_utils.apply_gaussian_noise", return_value="processed_image")
@patch("utils.img_utils.imread", return_value="raw_image")
@patch("utils.img_utils.imsave")
def test_process_image_known_method(mock_save, mock_read, mock_method, tmp_path):
    image_path = tmp_path / "input.png"
    image_path.write_text("dummy")  # Just to exist

    processed_path = tmp_path / "output.png"
    processing_data = {"method": "gaussian_noise"}

    img_utils.process_image(str(image_path), str(processed_path), processing_data)

    mock_method.assert_called_once_with("raw_image")
    mock_save.assert_called_once_with(str(processed_path), "processed_image")
