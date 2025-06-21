import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname("main.py"), "..")))
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # or wherever your FastAPI instance is

client = TestClient(app)

def test_check_progress():
    with patch("service.images_service.get_progress", return_value={"progress": 50}):
        response = client.get("/images/progress/")
        assert response.status_code == 200
        assert response.json() == {"status": "Esperando", "progress": 0}


# def test_upload_images_success():
#     mock_files = [("files", ("test.jpg", b"fake image content", "image/jpeg"))]
#     mock_processing_data = json.dumps({"methods": [{"image": "test.jpg", "method": "" }]})

#     with patch("service.images_service.process_images", new_callable=AsyncMock) as mock_process:
#         mock_process.return_value = {"message": "Processed successfully"}
#         response = client.post(
#             "/images/upload/",
#             data={"processing_data": mock_processing_data},
#             files=mock_files
#         )
#         assert response.status_code == 200
#         assert response.json() == {"message": "Processed successfully"}


def test_upload_images_invalid_json():
    mock_files = [("files", ("test.jpg", b"fake image content", "image/jpeg"))]
    # Invalid JSON string
    bad_json = '{"resize": true'  # missing closing }

    response = client.post(
        "/images/upload/",
        data={"processing_data": bad_json},
        files=mock_files
    )
    assert response.status_code == 500
    assert "Expecting" in response.json()["detail"]  # JSON decode error





def test_download_zip_not_found():
    with patch("service.images_service.get_zip", side_effect=FileNotFoundError):
        response = client.get("/images/download/missing_report")
        assert response.status_code == 404
        assert response.json() == {"detail": "ZIP file not found."}

