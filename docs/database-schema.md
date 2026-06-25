# Database Schema

The AI Recruiting Copilot backend uses PostgreSQL as the primary data store. The schema is built using SQLAlchemy 2.0 ORM. All primary keys are UUIDs, and tables feature soft-delete capability via `deleted_at`.

## Entity Relationship Diagram

```mermaid
erDiagram
    CANDIDATES ||--o{ CANDIDATE_DOCUMENTS : owns
    CANDIDATE_DOCUMENTS ||--o{ AI_EXTRACTIONS : has
    CANDIDATES ||--o{ CANDIDATE_SKILLS : has
    CANDIDATES ||--o{ CANDIDATE_EDUCATION : has
    CANDIDATES ||--o{ CANDIDATE_EXPERIENCE : has
    CANDIDATES ||--o{ CANDIDATE_PROJECTS : has
    
    CANDIDATES {
        uuid id PK
        enum status
        varchar first_name
        varchar last_name
        varchar email
        varchar phone
        text summary
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }
    
    CANDIDATE_DOCUMENTS {
        uuid id PK
        uuid candidate_id FK
        varchar file_path
        varchar file_type
        varchar original_name
        varchar storage_key
        text raw_text
        text extracted_text
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    AI_EXTRACTIONS {
        uuid id PK
        uuid document_id FK
        varchar provider
        varchar model_name
        varchar prompt_version
        varchar schema_version
        jsonb raw_ai_response
        jsonb normalized_response
        float confidence_score
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    BACKGROUND_JOBS {
        uuid id PK
        varchar job_type
        varchar correlation_id
        enum status
        jsonb payload
        jsonb result
        text error_message
        datetime started_at
        datetime completed_at
        datetime created_at
        datetime updated_at
    }
```
