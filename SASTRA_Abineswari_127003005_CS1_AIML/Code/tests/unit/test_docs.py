import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_project():
    response = client.post("/api/v1/projects/", json={"name": "Test Project", "description": "A test project"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"

def test_get_projects():
    response = client.get("/api/v1/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_invalid_file():
    # Attempt to upload a non-pdf file
    # First get a project
    response = client.post("/api/v1/projects/", json={"name": "Upload Test Project"})
    project_id = response.json()["id"]

    files = {"file": ("test.txt", b"dummy content", "text/plain")}
    response = client.post(f"/api/v1/projects/{project_id}/documents", files=files)
    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]

def test_upload_empty_file():
    response = client.post("/api/v1/projects/", json={"name": "Empty Upload Test Project"})
    project_id = response.json()["id"]

    files = {"file": ("empty.pdf", b"", "application/pdf")}
    response = client.post(f"/api/v1/projects/{project_id}/documents", files=files)
    assert response.status_code == 400
    assert "empty (0 bytes)" in response.json()["detail"]

def test_upload_corrupted_pdf():
    response = client.post("/api/v1/projects/", json={"name": "Corrupted Upload Test Project"})
    project_id = response.json()["id"]

    files = {"file": ("corrupted.pdf", b"NOT_A_REAL_PDF_HEADER_CONTENT", "application/pdf")}
    response = client.post(f"/api/v1/projects/{project_id}/documents", files=files)
    assert response.status_code == 400
    assert "Invalid or corrupted PDF file" in response.json()["detail"]

def test_system_config_endpoint():
    response = client.get("/api/v1/settings/system")
    assert response.status_code == 200
    data = response.json()
    assert "llm_provider" in data
    assert "llm_model" in data
    assert "has_api_key" in data
    assert isinstance(data["has_api_key"], bool)
    # Ensure no raw secret key is present in output keys
    assert "LLM_API_KEY" not in data
    assert "APP_SECRET_KEY" not in data
