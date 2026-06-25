from uuid import uuid4

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_resume(client):
    files = {"file": ("test.pdf", b"dummy content", "application/pdf")}
    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 202
    data = response.json()
    assert "ingestion_id" in data
    assert "document_id" in data

def test_upload_resume_invalid_type(client):
    files = {"file": ("test.txt", b"dummy content", "text/plain")}
    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 400

def test_get_document_metadata(client):
    id_str = str(uuid4())
    response = client.get(f"/api/v1/documents/{id_str}")
    assert response.status_code == 200

def test_get_document_status(client):
    id_str = str(uuid4())
    response = client.get(f"/api/v1/documents/{id_str}/status")
    assert response.status_code == 200

def test_download_document(client):
    id_str = str(uuid4())
    response = client.get(f"/api/v1/documents/{id_str}/download")
    assert response.status_code == 200
    assert response.content == b"mock bytes"

def test_get_job(client):
    id_str = str(uuid4())
    response = client.get(f"/api/v1/jobs/{id_str}")
    assert response.status_code == 200

def test_update_job(client):
    id_str = str(uuid4())
    response = client.patch(f"/api/v1/jobs/{id_str}", json={"status": "RUNNING"})
    assert response.status_code == 200

def test_list_candidates(client):
    response = client.get("/api/v1/candidates")
    assert response.status_code == 200

def test_get_candidate(client):
    id_str = str(uuid4())
    response = client.get(f"/api/v1/candidates/{id_str}")
    assert response.status_code == 200

def test_get_candidate_documents(client):
    id_str = str(uuid4())
    response = client.get(f"/api/v1/candidates/{id_str}/documents")
    assert response.status_code == 200
