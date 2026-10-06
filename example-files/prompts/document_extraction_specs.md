# Build a PDF Document Extraction App Using a Vision Model

Build an MVP web application for **extracting user-defined fields from PDF documents using a configurable Vision/Multimodal LLM**. Only PDF files supported. Design with clean architecture so additional file types can be added later.

---

## 1. Workflow

```text
Configure Vision Model → Upload PDF → Define Fields → Run Extraction → View Results → Download
```

Simple enough for a non-technical user.

---

## 2. Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Backend**: Python, FastAPI, Pydantic, Uvicorn
- **PDF Processing**: PyMuPDF (`fitz`) — isolated from extraction logic
- **Object Storage**: MinIO — persistent storage for uploaded PDF documents
  - MinIO and PostgreSQL settings are read from environment variables. For local testing and hosting, use **pgsty/silo** as the MinIO alternative (S3-compatible; same `MINIO_*` env vars and the same client code).
  - App code must not reference Silo specifically. The packaged app does not bundle any object storage; when deployed on a target setup it uses that setup's MinIO, configured only through `MINIO_*` env vars.
- **Database**: PostgreSQL — persistent storage for document metadata and extracted data
- **ORM / Migrations**: SQLAlchemy 2.x + Alembic

---

## 3. Application UI

Clean enterprise-style UI with two pages:

```text
┌──────────────────────────────┐
│ Settings                     │
│ Document Extraction          │
└──────────────────────────────┘
```

Default page: **Settings**, so the user configures the Vision Model before attempting extraction.

---

## 4. Document Extraction Page

```text
┌─────────────────────────────────────────────────────────┐
│                  Document Extraction                    │
├───────────────────────────┬─────────────────────────────┤
│                           │                             │
│      PDF Preview          │     Extraction Fields       │
│                           │                             │
│                           │     [Field configuration]   │
│                           │                             │
│                           │     [Extract Document]      │
│                           │                             │
├───────────────────────────┴─────────────────────────────┤
│                   Extraction Results                     │
└─────────────────────────────────────────────────────────┘
```

Layout can be adjusted for screen size.

---

## 5. PDF Upload

Drag-and-drop upload area. Only accept `application/pdf`.

```text
Upload PDF Document

Drag & drop a PDF here
or

[ Browse PDF ]

Maximum file size: configurable
```

After upload display: filename, file size, number of pages, upload status, remove/replace button.

Reject any non-PDF file with: "Only PDF documents are supported."

---

## 5A. Document Storage — MinIO

All uploaded PDF documents must be stored persistently in **MinIO**.

### Requirements

- MinIO is the system of record for the uploaded PDF binary.
- Do **not** store PDF binary content in PostgreSQL.
- Do **not** depend on the local filesystem for persistent document storage.
- After validation, upload the original PDF to MinIO.
- Keep the original PDF in MinIO after extraction so it can be reopened and processed again.
- Generate a unique `document_id` for every uploaded document.
- Use an object key such as `documents/{document_id}/original.pdf`.
- Keep bucket names configurable.
- Never expose MinIO credentials to the frontend.
- Retrieve documents through the backend or short-lived authenticated/presigned URLs.
- Temporary local files may be used by PyMuPDF when required, but must be cleaned up after processing.

### MinIO Configuration

```env
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false
MINIO_BUCKET_DOCUMENTS=documents
```

Example values are for development only.

### Storage Abstraction

Create an `ObjectStorage` abstraction with:

```text
upload()
download()
delete()
exists()
generate_presigned_url()
```

Implement `MinIOObjectStorage`.

Application services should depend on `ObjectStorage`, not directly on MinIO client calls.

### Upload Workflow

```text
Receive PDF
    ↓
Validate file type and size
    ↓
Validate PDF
    ↓
Generate document_id
    ↓
Upload original PDF to MinIO
    ↓
Create document metadata in PostgreSQL
    ↓
Return document_id
```

If MinIO upload fails, do not create a successfully uploaded document record.

If PostgreSQL persistence fails after a successful MinIO upload, explicitly handle the inconsistency by cleaning up the object or marking the document state appropriately. Do not silently lose track of uploaded objects.

### Document Deletion

When a document is deleted:

1. Delete its PDF object from MinIO.
2. Delete or appropriately cascade its PostgreSQL metadata and extraction records.
3. Do not leave orphaned persistent objects or database records.

---

## 5B. PostgreSQL Database

Use **PostgreSQL** as the persistent database for all structured data related to documents and extracted data.

### Requirements

- PostgreSQL is the primary application database.
- Do not use SQLite as the application database.
- Do not store PDF binary data in PostgreSQL.
- Store document metadata, extraction definitions, extraction runs, field results, evidence, confidence, validation state, and verification/edit information in PostgreSQL.
- Use SQLAlchemy 2.x.
- Use Alembic for migrations.
- Use UUIDs for document and extraction identifiers.
- Use JSONB for flexible structured data such as evidence, bounding boxes, normalized values, or model metadata.

### Suggested Models

#### Document

```text
Document
--------
id                  UUID PRIMARY KEY
original_filename   VARCHAR
mime_type           VARCHAR
file_size           BIGINT
page_count          INTEGER
minio_bucket        VARCHAR
minio_object_key    VARCHAR
document_type       VARCHAR NULL
status              VARCHAR
created_at          TIMESTAMP
updated_at          TIMESTAMP
```

Document status:

```text
UPLOADING
UPLOADED
PROCESSING
COMPLETED
FAILED
DELETED
```

#### Extraction

```text
Extraction
----------
id                  UUID PRIMARY KEY
document_id         UUID FOREIGN KEY
status              VARCHAR
model_provider      VARCHAR
model_name          VARCHAR
instructions        TEXT
processing_time_ms  BIGINT
fields_requested    INTEGER
fields_extracted    INTEGER
fields_not_found    INTEGER
validation_failures INTEGER
created_at          TIMESTAMP
completed_at        TIMESTAMP NULL
```

Extraction status:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

#### ExtractionField

```text
ExtractionField
---------------
id                  UUID PRIMARY KEY
extraction_id       UUID FOREIGN KEY
name                VARCHAR
display_name        VARCHAR
description         TEXT
data_type           VARCHAR
required            BOOLEAN
sort_order          INTEGER
```

#### ExtractionResult

```text
ExtractionResult
----------------
id                  UUID PRIMARY KEY
extraction_id       UUID FOREIGN KEY
field_id            UUID FOREIGN KEY
value               JSONB
normalized_value    JSONB NULL
confidence          DECIMAL NULL
status              VARCHAR
page                INTEGER NULL
document_section    VARCHAR NULL
evidence            TEXT NULL
bounding_box        JSONB NULL
validation_status   VARCHAR NULL
is_verified         BOOLEAN
is_user_edited      BOOLEAN
original_value      JSONB NULL
edited_value        JSONB NULL
created_at          TIMESTAMP
updated_at          TIMESTAMP
```

### Optional Document Sections

If document classification/section detection is implemented:

```text
DocumentSection
---------------
id                  UUID PRIMARY KEY
document_id         UUID FOREIGN KEY
section_type        VARCHAR
start_page          INTEGER
end_page            INTEGER
metadata            JSONB
created_at          TIMESTAMP
```

Do not hardcode document-specific section types.

### Relationships

```text
Document
   │
   ├──< Extraction
   │       │
   │       ├──< ExtractionField
   │       │
   │       └──< ExtractionResult
   │
   └──< DocumentSection
```

A document can have multiple extraction runs.

**Do not overwrite previous extraction results by default.** Each **Extract Again** operation should create a new extraction record so previous runs remain available.

### Persistence

The following must survive backend restarts:

- Document metadata
- MinIO object reference
- Document status
- Page count
- Extraction runs
- User-defined field definitions
- Extraction results
- Confidence
- Page numbers
- Evidence
- Validation state
- User verification/edit state
- Timestamps and processing metrics

Create an initial Alembic migration and support:

```text
alembic upgrade head
```

PostgreSQL and MinIO are externally available services. **Do not introduce Docker Compose, Kubernetes, or another deployment technology as a requirement.**


---

## 6. PDF Preview

```text
PDF Preview

┌────────┐
│ Page 1 │
│        │
│ PDF    │
│        │
└────────┘

Page 1 of 5

[ Previous ] [ Next ]
```

Render PDF pages, show page number, allow navigation, zoom if practical. Simple page-by-page preview for MVP.

---

## 7. Fields to Extract

User defines arbitrary fields. Each field has: Field Name, Description, Data Type, Required.

```text
Fields to Extract

┌─────────────────────────────────────────────────────┐
│ Field Name: Policy Number                            │
│ Description: Extract the policy number              │
│ Type: String                                         │
│ Required: Yes                                        │
│                                                     │
│                                      [Remove]        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Field Name: Patient Name                             │
│ Description: Full name of the patient               │
│ Type: String                                         │
│ Required: Yes                                        │
│                                                     │
│                                      [Remove]        │
└─────────────────────────────────────────────────────┘

[ + Add Field ]
```

The above fields are only UI examples. Do not hardcode them.

Supported data types: String, Integer, Decimal, Date, Boolean, Email, Phone, Currency.

---

## 8. Additional Instructions

Optional editable textarea:

```text
Extract only information that is present in the document.

Do not guess or hallucinate values.

If a requested field cannot be found, return null.

Preserve the value as it appears in the document unless
normalization is explicitly requested.
```

---

## 9. Extract Document

```text
[ Extract Document ]
```

Before extraction validate: PDF uploaded, PDF valid, at least one named field, model configured.

Progress display:

```text
Preparing PDF...
      ↓
Rendering PDF pages...
      ↓
Sending document to Vision Model...
      ↓
Processing extraction...
      ↓
Validating results...
```

UI must remain responsive.

---

## 10. Vision Model Architecture

Decouple the Vision Model via an abstract `VisionModelProvider` interface. Implement `OpenAICompatibleProvider` that works with any OpenAI-compatible vision API (vLLM, OpenAI, etc.). No model-specific logic in the extraction service.

The provider sends all rendered PDF pages as base64 PNG images in a single chat completion request. Handle auth errors (401), rate limits (429), timeouts, and malformed responses. Include truncated raw response snippets in error messages for diagnosis.

---

## 11. PDF Processing & Multi-Page Support

Render each PDF page as PNG at configurable DPI (default 150). Send all page images to Vision Model. Preserve page numbers in results.

PDF service: `validate_pdf()`, `get_page_count()`, `render_page()`, `render_all_pages()` — independent of provider.

Must support multi-page PDFs. If a field is found on Page 3, the result contains `"page": 3`.

---

## 12. Extraction Prompt & Response

Build a dynamic prompt: extract only requested fields, return null if not found, return valid JSON with `value`, `confidence`, `page`, `evidence` per field. Dynamically add user-defined fields with name, description, type, required.

Expected response:

```json
{
  "fields": [
    {
      "name": "policy_number",
      "value": "POL-123456",
      "confidence": 0.96,
      "page": 1,
      "evidence": "Policy Number: POL-123456"
    }
  ]
}
```

Validate with Pydantic. If invalid JSON: attempt cleanup (strip markdown fencing), re-validate, or return error. Never silently accept bad data.

---

## 13. Extraction Results UI

```text
Extraction Results

┌─────────────────┬───────────────────┬────────────┬────────┐
│ Field           │ Value             │ Confidence │ Page   │
├─────────────────┼───────────────────┼────────────┼────────┤
│ Policy Number   │ POL-123456        │ 96%        │ 1      │
│ Patient Name    │ John Doe          │ 98%        │ 1      │
│ Date of Birth   │ 15/04/1980        │ 94%        │ 2      │
│ Address         │ Hyderabad         │ 91%        │ 2      │
└─────────────────┴───────────────────┴────────────┴────────┘
```

For missing values:

```text
Patient Phone
Not Found
```

For low confidence:

```text
Address
Hyderabad, Telangana

⚠ Low Confidence: 61%
```

---

## 14. Source Evidence

If the model returns evidence, show it:

```text
Patient Name

John Doe

Confidence: 98%
Page: 1

Evidence:
"Patient Name: John Doe"
```

---

## 15. Results Actions

```text
[ Copy JSON ]
[ Download JSON ]
[ Download CSV ]
[ Extract Again ]
[ Clear ]
```

---

## 16. Settings Page

### Provider

```text
OpenAI Compatible
DKubeX (SecureLLM)
```

Both use the same OpenAI-compatible backend. When the user selects DKubeX and the base URL field is empty, auto-fill it with `https://<host>/securellm/v1`, where `<host>` is derived automatically in the browser as `window.location.host` (the hostname/port the app is currently being accessed through), and the scheme from `window.location.protocol` — do not hardcode a hostname or show a literal placeholder for the user to edit. This makes the same build work unmodified on any DKubeX deployment: a workspace tile is always served from the same host as the platform itself (just under a different path), so the currently-loaded page's origin is always the correct SecureLLM host. The field remains a normal editable text input in case a different SecureLLM endpoint is needed.

### Configuration

```text
Provider:
OpenAI Compatible

API Base URL:
http://localhost:8000/v1

API Key:
****************

Model:
Qwen3-VL-32B-Instruct

Temperature:
0

Max Tokens:
4096

Timeout:
120 seconds

PDF Rendering DPI:
150
```

Example values are illustrative only.

### Model Selection (Combobox)

The **Model** field works as both text input and dropdown:
- User can always type a model name manually
- **Fetch Models** button calls `{base_url}/models` and populates a dropdown with available model IDs (sorted)
- Typing filters the fetched list
- If fetch fails, show non-blocking error; user continues typing manually

Backend endpoint: `POST /api/settings/model/models` — takes `api_base_url` + `api_key`, calls `/models` with Bearer auth, returns model IDs from `data[].id`.

### Test Connection

```text
[ Test Connection ]
```

Verify endpoint connectivity, authentication, model availability. Display success/failure with response time:

```text
✓ Connection successful

Model: configured-model
Response time: 2.4 seconds
```

Never expose API keys.

---

## 17. Security

- Mask API keys in UI, never log them, never expose in responses or stack traces
- Do not log document contents or extracted values
- Provide `.env.example`, never commit real keys
- Persist settings to JSON file with `0600` permissions (configurable via `SETTINGS_FILE` env var) so they survive `uvicorn --reload`. Load from file on startup, fall back to `.env` defaults.
- Clean up only temporary local PDF/page files after processing; do not delete the persisted original PDF from MinIO
- Store document metadata and extracted structured data in PostgreSQL
- Store the original PDF binary only in MinIO

---

## 18. API Endpoints

```text
GET    /api/health

GET    /api/settings/model
PUT    /api/settings/model
POST   /api/settings/model/test
POST   /api/settings/model/models

POST   /api/documents/upload
GET    /api/documents/{document_id}
GET    /api/documents/{document_id}/pages/{page_num}
GET    /api/documents/{document_id}/download
DELETE /api/documents/{document_id}

POST   /api/extractions
GET    /api/extractions/{extraction_id}
GET    /api/extractions/{extraction_id}/result
GET    /api/extractions/{extraction_id}/download/json
GET    /api/extractions/{extraction_id}/download/csv
```

Use Pydantic request/response models.

---

## 19. Error Handling

Handle: invalid PDF, PDF too large, empty PDF, model not configured, invalid API key, model unavailable, network/model timeout, rate limit, invalid JSON, schema validation failure.

```text
Extraction Failed

The Vision Model did not return valid structured data.

[ Retry ]
```

Show friendly messages, no stack traces. Include truncated raw response snippet when model output can't be parsed.

---

## 20. Environment & Running

```env
APP_ENV=development
LOG_LEVEL=INFO
MAX_PDF_SIZE_MB=25
MODEL_PROVIDER=openai_compatible
MODEL_BASE_URL=http://localhost:8000/v1
MODEL_NAME=vision-model
MODEL_API_KEY=
MODEL_TIMEOUT=120
PDF_RENDER_DPI=150
SETTINGS_FILE=./.data/model_settings.json

DATABASE_URL=postgresql+asyncpg://document_extractor:document_extractor@localhost:5432/document_extractor

# Object storage: pgsty/silo (S3-compatible MinIO alternative) for local testing and hosting.
# On a target setup, point these at that setup's MinIO.
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false
MINIO_BUCKET_DOCUMENTS=documents
```

Run locally without Docker. Backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000`. Frontend: `npm run dev`. Frontend proxies `/api` to backend. Ports configurable.

---

## 21. Testing

No real API key required. Generate synthetic PDFs programmatically, mock Vision Model responses.

Test: PDF service (valid/invalid/empty/multi-page, rendering, size limits), prompt builder, schema validator (valid/invalid/markdown-fenced JSON, missing fields, confidence), provider (mocked: success, auth error, timeout, bad response), API endpoints (upload, settings, test connection, extraction, downloads), frontend components (upload, field editor, results, settings).

Persistence integration test:
1. Upload a PDF.
2. Verify the original PDF exists in MinIO.
3. Verify document metadata exists in PostgreSQL.
4. Run extraction.
5. Verify extraction, field definitions, and results exist in PostgreSQL.
6. Restart the backend.
7. Retrieve the document and results again.
8. Verify the PDF remains available from MinIO and structured data remains available.
9. Run Extract Again and verify a new extraction run is created without overwriting the previous run.

---

## 22. Logging & README

Structured logging: request_id, operation, filename, page_count, model, processing_time, status. Track duration for upload, rendering, model request, validation. Never log API keys, PDF contents, or extracted values.

Create a concise README: what it does, architecture, tech stack, installation, running, model configuration, API overview, testing, troubleshooting.

---

## 23. Build & Verify

Build the actual working application. Use mocks only for automated tests. Keep provider-specific code isolated from PDF processing.

After building, run all tests, lint/type checks, and verify the full workflow using **pgsty/silo** as the object store:

```text
Settings → Configure Model → Test Connection → Upload PDF → Persist to MinIO → Add Fields → Extract → Persist Results to PostgreSQL → View Results → Download JSON/CSV
```
