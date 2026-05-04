# API Reference

Complete REST API documentation for MortIQ.

## Base URL

```
http://localhost:5300
```

For DKubeX deployments, the base path is configurable via `DKUBEX_BASE_PATH` environment variable.

## Authentication

MortIQ supports DKubeX authentication via headers:

```http
X-Auth-Request-User: username
X-Auth-Request-Email: user@example.com
X-Auth-Request-Role: admin
X-Auth-Request-User-Namespace: default
```

## Common Response Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Applications API

### List Applications

```http
GET /api/applications
```

**Query Parameters:**
- `status` (optional) - Filter by status: `intake`, `extracting`, `under_review`, `flagged`, `approved`, `closed`
- `loan_type` (optional) - Filter by loan type: `purchase`, `refinance`, `heloc`, `fha`
- `limit` (optional) - Number of results (default: 50)
- `offset` (optional) - Pagination offset (default: 0)

**Response:**
```json
{
  "applications": [
    {
      "id": "uuid",
      "applicant_name": "John Smith",
      "loan_type": "purchase",
      "loan_amount": 350000,
      "property_value": 450000,
      "status": "approved",
      "broker_name": "Jane Broker",
      "priority": "normal",
      "dti_ratio": 0.35,
      "ltv_ratio": 0.78,
      "current_agent": null,
      "pipeline_stage": "completed",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T11:45:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### Get Application Details

```http
GET /api/applications/{application_id}
```

**Response:**
```json
{
  "id": "uuid",
  "applicant_name": "John Smith",
  "loan_type": "purchase",
  "loan_amount": 350000,
  "property_value": 450000,
  "status": "approved",
  "broker_name": "Jane Broker",
  "priority": "normal",
  "dti_ratio": 0.35,
  "ltv_ratio": 0.78,
  "current_agent": null,
  "pipeline_stage": "completed",
  "ai_mode": "claude",
  "pipeline_mode": "auto",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:45:00Z",
  "documents": [
    {
      "id": "uuid",
      "doc_type": "w2",
      "original_filename": "w2_2023.pdf",
      "page_count": 2,
      "extraction_status": "extracted",
      "confidence_avg": 0.95
    }
  ],
  "anomalies": [
    {
      "id": "uuid",
      "anomaly_type": "name_mismatch",
      "severity": "warning",
      "description": "Name variant detected",
      "status": "resolved",
      "tier": 1
    }
  ]
}
```

### Create Application

```http
POST /api/applications
Content-Type: application/json
```

**Request Body:**
```json
{
  "applicant_name": "John Smith",
  "loan_type": "purchase",
  "loan_amount": 350000,
  "property_value": 450000,
  "broker_name": "Jane Broker",
  "priority": "normal",
  "ai_mode": "claude"
}
```

**Response:**
```json
{
  "id": "uuid",
  "applicant_name": "John Smith",
  "status": "intake",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Application

```http
PUT /api/applications/{application_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "under_review",
  "priority": "urgent",
  "dti_ratio": 0.35,
  "ltv_ratio": 0.78
}
```

### Delete Application

```http
DELETE /api/applications/{application_id}
```

**Response:**
```json
{
  "message": "Application deleted successfully"
}
```

## Upload API

### Upload Documents

```http
POST /api/upload
Content-Type: multipart/form-data
```

**Form Data:**
- `application_id` - UUID of the application
- `files` - One or more files (PDF, PNG, JPG)

**Response:**
```json
{
  "application_id": "uuid",
  "uploaded_files": [
    {
      "document_id": "uuid",
      "filename": "w2_2023.pdf",
      "doc_type": "w2",
      "page_count": 2,
      "file_hash": "sha256hash"
    }
  ],
  "total_uploaded": 1
}
```

### Validate Files

```http
POST /api/upload/validate
Content-Type: multipart/form-data
```

**Form Data:**
- `files` - Files to validate

**Response:**
```json
{
  "valid_files": ["w2_2023.pdf"],
  "invalid_files": [],
  "errors": []
}
```

## Pipeline API

### Run Pipeline

```http
POST /api/pipeline/run/{application_id}
```

**Query Parameters:**
- `mode` (optional) - Pipeline mode: `auto` (default) or `manual`

**Response:**
```json
{
  "application_id": "uuid",
  "pipeline_stage": "intake",
  "status": "extracting",
  "message": "Pipeline started"
}
```

### Get Pipeline Status

```http
GET /api/pipeline/status/{application_id}
```

**Response:**
```json
{
  "application_id": "uuid",
  "pipeline_stage": "analyzing",
  "status": "extracting",
  "current_agent": "Ana",
  "pipeline_mode": "auto",
  "stages_completed": ["intake", "extracting", "validating"],
  "stages_remaining": ["analyzing", "compliance", "delivering"]
}
```

### Trigger Manual Stage

```http
POST /api/pipeline/trigger/{application_id}/{stage}
```

**Path Parameters:**
- `stage` - Stage to trigger: `intake`, `extracting`, `validating`, `analyzing`, `compliance`, `delivering`

**Response:**
```json
{
  "application_id": "uuid",
  "stage": "compliance",
  "status": "triggered",
  "message": "Stage triggered successfully"
}
```

## Anomalies API

### List Anomalies

```http
GET /api/anomalies
```

**Query Parameters:**
- `application_id` (optional) - Filter by application
- `severity` (optional) - Filter by severity: `critical`, `warning`, `info`
- `status` (optional) - Filter by status: `open`, `resolved`, `false_positive`
- `tier` (optional) - Filter by tier: `1`, `2`, `3`

**Response:**
```json
{
  "anomalies": [
    {
      "id": "uuid",
      "application_id": "uuid",
      "document_id": "uuid",
      "anomaly_type": "ssn_conflict",
      "severity": "critical",
      "description": "Two different SSNs found: 123-45-6789 and 123-45-6780",
      "status": "open",
      "tier": 1,
      "created_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 1
}
```

### Get Anomaly Details

```http
GET /api/anomalies/{anomaly_id}
```

### Resolve Anomaly

```http
POST /api/anomalies/{anomaly_id}/resolve
Content-Type: application/json
```

**Request Body:**
```json
{
  "resolution": "Confirmed SSN 123-45-6789 is correct",
  "resolved_by": "underwriter@example.com"
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "resolved",
  "resolved_by": "underwriter@example.com",
  "resolved_at": "2024-01-15T11:00:00Z"
}
```

## Compliance API

### List Compliance Checks

```http
GET /api/compliance/{application_id}
```

**Response:**
```json
{
  "application_id": "uuid",
  "checks": [
    {
      "id": "uuid",
      "rule_id": 1,
      "rule_name": "Fannie Mae DTI Max",
      "category": "fannie_mae",
      "rule_type": "dti_max",
      "threshold_value": "43",
      "passed": true,
      "details": "DTI ratio 35% is below maximum 43%",
      "checked_at": "2024-01-15T11:30:00Z"
    }
  ],
  "total_checks": 15,
  "passed": 14,
  "failed": 1
}
```

### Get Compliance Rules

```http
GET /api/compliance/rules
```

**Query Parameters:**
- `category` (optional) - Filter by category: `fannie_mae`, `fha`, `va`, `freddie_mac`
- `rule_type` (optional) - Filter by type: `dti_max`, `ltv_max`, `credit_min`, `doc_required`

**Response:**
```json
{
  "rules": [
    {
      "id": 1,
      "name": "Fannie Mae DTI Max",
      "category": "fannie_mae",
      "rule_type": "dti_max",
      "threshold_value": "43",
      "description": "Maximum debt-to-income ratio for Fannie Mae conventional loans",
      "source": "Fannie Mae Selling Guide B3-6",
      "version": "2024"
    }
  ],
  "total": 15
}
```

## Reports API

### Generate Report

```http
GET /api/reports/{application_id}
```

**Query Parameters:**
- `format` (optional) - Response format: `json` (default) or `html`

**Response (JSON):**
```json
{
  "application_id": "uuid",
  "applicant_name": "John Smith",
  "executive_summary": "Application approved with no conditions...",
  "compliance_summary": {
    "total_checks": 15,
    "passed": 15,
    "failed": 0
  },
  "anomalies_summary": {
    "total": 0,
    "critical": 0,
    "warnings": 0,
    "info": 0
  },
  "recommendation": "APPROVED",
  "conditions": [],
  "generated_at": "2024-01-15T12:00:00Z"
}
```

### Download PDF Report

```http
GET /api/reports/{application_id}/pdf
```

**Response:**
- Content-Type: `application/pdf`
- Binary PDF file

## Metrics API

### System Metrics

```http
GET /api/metrics
```

**Response:**
```json
{
  "applications": {
    "total": 150,
    "by_status": {
      "intake": 5,
      "extracting": 3,
      "under_review": 8,
      "approved": 120,
      "flagged": 10,
      "closed": 4
    }
  },
  "anomalies": {
    "total": 45,
    "by_severity": {
      "critical": 5,
      "warning": 30,
      "info": 10
    }
  },
  "processing": {
    "avg_cycle_time_minutes": 4.2,
    "total_documents_processed": 1200,
    "avg_documents_per_application": 8
  },
  "costs": {
    "total_api_cost_usd": "18.50",
    "avg_cost_per_application": "0.12"
  }
}
```

### Agent Performance

```http
GET /api/metrics/agents
```

**Response:**
```json
{
  "agents": [
    {
      "name": "Iris",
      "role": "intake",
      "status": "idle",
      "total_processed": 150,
      "avg_processing_time_seconds": 5,
      "last_completed_at": "2024-01-15T11:45:00Z",
      "error_count": 0
    },
    {
      "name": "Rex",
      "role": "extractor",
      "status": "active",
      "current_application_id": "uuid",
      "total_processed": 148,
      "avg_processing_time_seconds": 45,
      "last_completed_at": "2024-01-15T11:40:00Z",
      "error_count": 2
    }
  ]
}
```

## Health & Status API

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "app": "mortiq"
}
```

### User Info (DKubeX)

```http
GET /api/whoami
```

**Response:**
```json
{
  "user": "john.smith",
  "email": "john.smith@example.com",
  "role": "admin",
  "namespace": "default"
}
```

## WebSocket Events

### Connect to Event Stream

```javascript
const ws = new WebSocket('ws://localhost:5300/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Event:', data);
};
```

### Event Types

#### Agent Events
```json
{
  "channel": "agents",
  "event": "agent.active",
  "data": {
    "agent": "Rex",
    "application": "John Smith",
    "application_id": "uuid"
  }
}
```

```json
{
  "channel": "agents",
  "event": "agent.completed",
  "data": {
    "agent": "Rex",
    "application": "John Smith",
    "application_id": "uuid"
  }
}
```

#### Pipeline Events
```json
{
  "channel": "pipeline",
  "event": "pipeline.stage_changed",
  "data": {
    "application_id": "uuid",
    "stage": "analyzing",
    "status": "extracting"
  }
}
```

#### Anomaly Events
```json
{
  "channel": "anomalies",
  "event": "anomaly.detected",
  "data": {
    "anomaly_id": "uuid",
    "application_id": "uuid",
    "severity": "critical",
    "type": "ssn_conflict"
  }
}
```

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message",
  "detail": "Detailed error description",
  "status_code": 400
}
```

### Common Errors

**400 Bad Request**
```json
{
  "error": "Invalid request",
  "detail": "Missing required field: applicant_name"
}
```

**404 Not Found**
```json
{
  "error": "Not found",
  "detail": "Application with id 'uuid' not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "detail": "Database connection failed"
}
```

## Rate Limiting

Currently, no rate limiting is enforced. For production deployments, consider implementing rate limiting at the ingress level.

## API Versioning

The current API is version 1.0. Future versions will be indicated in the URL path:

```
/api/v2/applications
```

## SDK Examples

### Python
```python
import httpx

async with httpx.AsyncClient() as client:
    # Create application
    response = await client.post(
        "http://localhost:5300/api/applications",
        json={
            "applicant_name": "John Smith",
            "loan_type": "purchase",
            "loan_amount": 350000,
            "property_value": 450000
        }
    )
    app = response.json()
    
    # Run pipeline
    await client.post(
        f"http://localhost:5300/api/pipeline/run/{app['id']}"
    )
```

### JavaScript
```javascript
// Create application
const response = await fetch('http://localhost:5300/api/applications', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    applicant_name: 'John Smith',
    loan_type: 'purchase',
    loan_amount: 350000,
    property_value: 450000
  })
});
const app = await response.json();

// Run pipeline
await fetch(`http://localhost:5300/api/pipeline/run/${app.id}`, {
  method: 'POST'
});
```

### cURL
```bash
# Create application
curl -X POST http://localhost:5300/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_name": "John Smith",
    "loan_type": "purchase",
    "loan_amount": 350000,
    "property_value": 450000
  }'

# Run pipeline
curl -X POST http://localhost:5300/api/pipeline/run/{application_id}
```

## Support

For API support and questions, please refer to the project repository or contact the development team.
