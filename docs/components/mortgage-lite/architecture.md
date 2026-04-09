# Mortgage-Lite Architecture

This document describes the system architecture, design principles, and component interactions of Mortgage-Lite.

## System Overview

Mortgage-Lite is a multi-agent AI system designed for automated mortgage underwriting with privacy-first principles. The architecture separates concerns into distinct processing zones based on data sensitivity.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  Browser (HTMX + TailwindCSS) ←→ WebSocket (Real-time Events)  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                         │
│  REST Endpoints │ Upload │ Pipeline │ Reports │ Metrics         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT PIPELINE                              │
│                                                                   │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌────────┐  ┌──────┐ │
│  │ Iris │→│ Rex  │→│ Val  │→│ Ana  │→│ Claire │→│ Max  │ │
│  └──────┘  └──────┘  └──────┘  └──────┘  └────────┘  └──────┘ │
│  Classify   Extract   Validate  Analyze   Comply     Deliver    │
│                                                                   │
│           ↑ LOCAL ZONE ↑    │ ANONYMIZE │  ↑ CLOUD ZONE ↑      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│  PostgreSQL/SQLite │ File Storage │ Audit Logs                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agent Pipeline

The pipeline consists of six specialized agents that process applications sequentially:

#### Iris (Intake Agent)
- **Role**: Document classification and intake
- **Processing**: Local
- **Functions**:
  - Receives uploaded files
  - Classifies document types (W-2, 1099, bank statements, etc.)
  - Validates file integrity
  - Creates Document records
  - Sets application status to `extracting`

#### Rex (Extractor Agent)
- **Role**: OCR and data extraction
- **Processing**: Local
- **Functions**:
  - Multi-engine OCR cascade:
    1. GLM-OCR (0.9B, specialized)
    2. MiniCPM-V (8B, document understanding)
    3. Qwen2-VL (2B, fast tables)
    4. Tesseract (fallback)
    5. PDF text extraction (digital PDFs)
  - Extracts structured fields per document type
  - Generates confidence scores and bounding boxes
  - Converts tables to Pandas DataFrames
  - Creates ExtractedField records

#### Val (Validator Agent)
- **Role**: Deterministic validation (shift-left)
- **Processing**: Local, no AI/LLM
- **Functions**:
  - Pure Python deterministic checks (zero AI cost)
  - Counts unique SSNs across documents → CRITICAL if >1
  - Detects name variants → WARNING
  - Validates table math (column sums) → WARNING
  - Checks for missing required documents
  - Verifies loan amounts vs limits
  - Creates Anomaly records with tier=1
  - Flags applications for CRITICAL issues
  - Sends Telegram alerts for critical anomalies

#### Ana (Analyzer Agent)
- **Role**: Contextual analysis with local LLM
- **Processing**: Local (Ollama/Qwen)
- **Functions**:
  - Uses local LLM (Qwen 3.5 35B, Nemotron, etc.)
  - Operates on RAW unredacted data (local = secure)
  - Finds contextual anomalies:
    - Phonetic name mismatches
    - Employment gaps
    - Unexplained deposits
    - Income inconsistencies
  - Cross-references extracted fields
  - Creates Anomaly records with tier=2
  - Calculates preliminary DTI and LTV ratios
  - **Prepares anonymization mapping**

#### Claire (Compliance Agent)
- **Role**: Compliance checking and synthesis
- **Processing**: Cloud (Claude), anonymized data only
- **Functions**:
  - Receives ONLY anonymized JSON (never sees real PII)
  - Runs compliance checks against 15+ rules:
    - Fannie Mae guidelines
    - FHA requirements
    - VA loan rules
    - Freddie Mac standards
  - Calculates DTI and LTV from anonymized data
  - Generates executive summary with Claude
  - Cross-document synthesis
  - Cites regulatory guidelines
  - Recommends: approve / conditional / deny
  - Creates ComplianceCheck records

#### Max (Messenger Agent)
- **Role**: Final delivery and notifications
- **Processing**: Local
- **Functions**:
  - Receives deanonymized final report
  - Sets final application status
  - Generates AuditLog entries with hash chain
  - Pushes to bank's LOS (Encompass API)
  - Sends Telegram notifications
  - Triggers voice callbacks (Nancy integration)
  - Executes data death protocol (cleanup)

### 2. Privacy Boundaries

#### Anonymization Boundary (Ana → Claire)
```python
# Before Claire processing
{
  "applicant_name": "Catherine Vellotti" → "[APPLICANT_1]",
  "ssn": "123-45-6789" → "[SSN_1]",
  "address": "1247 Oak St, Austin, TX" → "[ADDRESS_1]",
  "employer": "TechSphere LLC" → "[EMPLOYER_1]",
  "income": 120000  # Unchanged - not PII without identity
}
```

#### Deanonymization Boundary (Claire → Max)
```python
# After Claire processing
{
  "[APPLICANT_1]" → "Catherine Vellotti",
  "[SSN_1]" → "123-45-6789",
  "[ADDRESS_1]" → "1247 Oak St, Austin, TX",
  "[EMPLOYER_1]" → "TechSphere LLC"
}
# Mapping PURGED permanently after deanonymization
```

### 3. Data Models

#### Application
Core entity representing a mortgage application:
- Applicant information
- Loan details (type, amount, property value)
- Status tracking (intake → extracting → under_review → flagged/approved/closed)
- Pipeline stage and mode
- DTI and LTV ratios
- AI mode selection

#### Document
Uploaded files associated with an application:
- Document type classification
- File metadata (path, hash, page count)
- Extraction status
- Average confidence score

#### ExtractedField
Structured data extracted from documents:
- Field name and value
- Confidence score
- Bounding box coordinates
- Page number

#### Anomaly
Issues detected during processing:
- Type (name_mismatch, ssn_conflict, math_error, etc.)
- Severity (critical, warning, info)
- Status (open, resolved, false_positive)
- Tier (1=deterministic, 2=local LLM, 3=cloud LLM)

#### ComplianceCheck
Regulatory compliance verification:
- Rule reference
- Pass/fail status
- Details and explanations

#### AuditLog
Complete audit trail:
- Event type and actor
- Payload and details
- Hash chain for integrity

### 4. API Layer

FastAPI-based REST API with the following routers:

#### Pages Router
- Dashboard (`/`)
- Applications Kanban (`/applications`)
- Upload interface (`/upload`)
- Settings (`/settings`)

#### Applications Router
- List applications (`GET /api/applications`)
- Get application details (`GET /api/applications/{id}`)
- Update application (`PUT /api/applications/{id}`)
- Delete application (`DELETE /api/applications/{id}`)

#### Pipeline Router
- Run pipeline (`POST /api/pipeline/run/{application_id}`)
- Get pipeline status (`GET /api/pipeline/status/{application_id}`)
- Manual stage trigger (`POST /api/pipeline/trigger/{application_id}/{stage}`)

#### Upload Router
- Upload documents (`POST /api/upload`)
- Validate files (`POST /api/upload/validate`)

#### Anomalies Router
- List anomalies (`GET /api/anomalies`)
- Get anomaly details (`GET /api/anomalies/{id}`)
- Resolve anomaly (`POST /api/anomalies/{id}/resolve`)

#### Compliance Router
- List compliance checks (`GET /api/compliance/{application_id}`)
- Get compliance rules (`GET /api/compliance/rules`)

#### Reports Router
- Generate report (`GET /api/reports/{application_id}`)
- Download PDF (`GET /api/reports/{application_id}/pdf`)

#### Metrics Router
- System metrics (`GET /api/metrics`)
- Agent performance (`GET /api/metrics/agents`)

### 5. Event System

Real-time event bus for UI updates:

```python
# Event types
- "agent.active" - Agent starts processing
- "agent.completed" - Agent finishes
- "agent.error" - Agent encounters error
- "pipeline.stage_changed" - Pipeline advances
- "anomaly.detected" - New anomaly found
- "application.status_changed" - Status update
```

### 6. Database Schema

#### Core Tables
- `applications` - Application records
- `documents` - Uploaded files
- `extracted_fields` - OCR results
- `anomalies` - Detected issues
- `agents` - Agent status
- `compliance_rules` - Regulatory rules
- `compliance_checks` - Compliance results
- `audit_log` - Complete audit trail
- `token_usage` - AI cost tracking
- `settings` - System configuration

#### Relationships
```
Application (1) ←→ (N) Document
Document (1) ←→ (N) ExtractedField
Application (1) ←→ (N) Anomaly
Application (1) ←→ (N) ComplianceCheck
Application (1) ←→ (N) AuditLog
```

## Design Principles

### 1. Privacy-First
- **Local Processing**: Sensitive data stays on-premises
- **Anonymization**: PII removed before cloud processing
- **Ephemeral Mappings**: Destroyed after use
- **Audit Trail**: Complete tracking of data access

### 2. Shift-Left Validation
- **Deterministic First**: Catch errors with zero-cost Python checks
- **Local LLM Second**: Use on-premises AI for contextual analysis
- **Cloud LLM Last**: Only for complex synthesis with anonymized data

### 3. Cost Optimization
- **Tiered Processing**: Route to appropriate model based on complexity
- **Parallel Execution**: Process multiple documents concurrently
- **Intelligent Caching**: Reuse results when possible
- **Token Tracking**: Monitor and optimize AI costs

### 4. Reliability
- **Fault Tolerance**: Retry logic for transient failures
- **Graceful Degradation**: Fallback to alternative models
- **State Management**: Resume from failure points
- **Health Monitoring**: Track agent and system health

### 5. Observability
- **Event Streaming**: Real-time pipeline visibility
- **Audit Logging**: Complete processing history
- **Metrics Collection**: Performance and cost tracking
- **Alert System**: Proactive issue notification

## Deployment Architecture

### Development
```
┌─────────────────┐
│   Local Machine │
│                 │
│  ┌───────────┐  │
│  │ FastAPI   │  │
│  │ (port 5300)│ │
│  └───────────┘  │
│       ↓         │
│  ┌───────────┐  │
│  │  SQLite   │  │
│  └───────────┘  │
│       ↓         │
│  ┌───────────┐  │
│  │  Ollama   │  │
│  │ (port 11434)│ │
│  └───────────┘  │
└─────────────────┘
```

### Production (Kubernetes)
```
┌──────────────────────────────────────────┐
│            Kubernetes Cluster             │
│                                           │
│  ┌────────────────────────────────────┐  │
│  │         Ingress Controller          │  │
│  │    (DKubeX Auth Middleware)        │  │
│  └────────────────────────────────────┘  │
│                   ↓                       │
│  ┌────────────────────────────────────┐  │
│  │    Mortgage-Lite Deployment        │  │
│  │    (replicas: 3)                   │  │
│  │                                     │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  FastAPI Container           │  │  │
│  │  │  - Port 5300                 │  │  │
│  │  │  - Health checks             │  │  │
│  │  │  - Resource limits           │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
│                   ↓                       │
│  ┌────────────────────────────────────┐  │
│  │    PostgreSQL StatefulSet          │  │
│  │    (persistent storage)            │  │
│  └────────────────────────────────────┘  │
│                   ↓                       │
│  ┌────────────────────────────────────┐  │
│  │    Ollama Service                  │  │
│  │    (GPU nodes)                     │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## Security Considerations

### Authentication
- DKubeX auth headers (`X-Auth-Request-User`, etc.)
- Role-based access control
- Namespace isolation

### Data Protection
- PII anonymization before cloud processing
- Encrypted storage (at rest)
- TLS for data in transit
- Ephemeral mapping destruction

### Audit & Compliance
- Complete audit trail with hash chain
- Immutable log records
- Regulatory compliance tracking
- Data retention policies

## Performance Characteristics

### Throughput
- **Target**: 60 applications/hour
- **Current**: ~15 applications/hour (4x improvement planned)

### Latency
- **Average Processing Time**: 4 minutes per application
- **Industry Standard**: 4 days per application

### Cost
- **Claude API**: ~$0.04 per application (with anonymization)
- **Local LLM**: Zero marginal cost
- **Total**: 60% reduction vs cloud-only approach

### Scalability
- **Horizontal**: Multiple FastAPI replicas
- **Vertical**: GPU nodes for Ollama
- **Database**: PostgreSQL with connection pooling

## Future Enhancements

### Planned Features
- Enhanced monitoring dashboard
- Advanced anomaly detection
- Multi-tenant support
- API rate limiting
- Webhook integrations
- Mobile app support

### Performance Improvements
- Adaptive model selection
- Intelligent stage routing
- Advanced caching strategies
- Optimized parallel processing

See the [Development Guide](../internal/development.md) for implementation details.
