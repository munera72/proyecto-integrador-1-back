import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from service import images_service
from pathlib import Path

@pytest.fixture(autouse=True)
def reset_progress():
    images_service.set_progress("Esperando", 0)
    yield
    images_service.set_progress("Esperando", 0)


def test_set_and_get_progress():
    images_service.set_progress("Working", 42)
    progress = images_service.get_progress()
    assert progress == {"status": "Working", "progress": 42}


@patch("service.images_service.create_image_zip")
@patch("service.images_service.predict_and_save_masks", return_value=["temp_uploads/mask1.png"])
@patch("service.images_service.process_image")
@patch("service.images_service.validate_and_prepare_image")
@patch("service.images_service.settings.DEFAULT_TARGET_PATH", str(Path("tests/test_output")))
@pytest.mark.asyncio
async def test_process_images_success(
    mock_validate,
    mock_process,
    mock_predict,
    mock_zip
):
    # Fake UploadFile with a file-like object
    class FakeUploadFile:
        def __init__(self, filename):
            self.filename = filename
            self.file = MagicMock()
    
    files = [FakeUploadFile("img1.jpg")]

    processing_data = {
        "methods": [
            {"image": "img1.jpg", "method": "blur", "param": "some_value"}
        ]
    }

    result = await images_service.process_images(files, processing_data)

    assert result["message"].endswith("image(s) processed and saved succesfully.")
    assert "file_name" in result

    mock_validate.assert_called_once()
    mock_process.assert_called_once()
    mock_predict.assert_called_once()
    mock_zip.assert_called_once()


@patch("service.images_service.Path.exists", return_value=True)
@patch("service.images_service.settings.DEFAULT_TARGET_PATH", "tests/test_output")
def test_get_zip_exists(mock_exists):
    path = images_service.get_zip("images")
    assert path is not None


@patch("service.images_service.Path.exists", return_value=False)
@patch("service.images_service.settings.DEFAULT_TARGET_PATH", "tests/test_output")
def test_get_zip_not_found(mock_exists):
    with pytest.raises(FileNotFoundError):
        images_service.get_zip("missing_report")
