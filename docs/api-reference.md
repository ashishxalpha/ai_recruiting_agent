# API Reference - AI Recruiting Copilot

## Resumes

### `POST /api/v1/resumes/upload`
Upload a new resume for candidate ingestion.
- **Content-Type**: `multipart/form-data`
- **Payload**: `file` (PDF or DOCX, max 10MB)
- **Response**: `202 Accepted`
```json
{
  "ingestion_id": "uuid",
  "document_id": "uuid",
  "job_id": "uuid",
  "status": "QUEUED"
}
```

## Documents

### `GET /api/v1/documents/{id}`
Retrieve metadata for a candidate document.

### `GET /api/v1/documents/{id}/status`
Check the parsing and ingestion status of the document.
- **Response**: `ResumeIngestionRequest` entity with `status`.

### `GET /api/v1/documents/{id}/download`
Download the raw document.
- **Response**: File bytes.

## Jobs

### `GET /api/v1/jobs/{id}`
Retrieve the execution status of a background job.

### `PATCH /api/v1/jobs/{id}`
Update the execution status (useful for external workers like Celery to report back).

## Candidates

### `GET /api/v1/candidates`
List all extracted and populated candidates.

### `GET /api/v1/candidates/{id}`
Retrieve a full candidate profile with skills, experiences, and education.

### `GET /api/v1/candidates/{id}/documents`
Retrieve all documents associated with a candidate.
