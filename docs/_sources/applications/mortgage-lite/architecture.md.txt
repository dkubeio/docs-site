# Mortgage-Lite Architecture

This document describes the system architecture, design principles, and component interactions of Mortgage-Lite.

## System Overview

Mortgage-Lite is a multi-agent AI system designed for automated mortgage underwriting with privacy-first principles. The architecture separates concerns into distinct processing zones based on data sensitivity.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  Browser (HTMX + TailwindCSS) ←→ WebSocket (Real-time Events)  │
│  PDF Viewer │ Kanban Board │ Anomaly Inspector                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                         │
│  REST Endpoints │ Upload │ Pipeline │ Reports │ Metrics         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MULTI-PIPELINE ARCHITECTURE                    │
│                                                                   │
│  UNDERWRITING:                                                   │
│  Iris → Rex → Val → Ana → [ANONYMIZE] → Claire → Max           │
│                                                                   │
│  SERVICING:                                                      │
│  Iris → Rex → Servo → Max                                       │
│                                                                   │
│  QUALITY CONTROL:                                                │
│  Iris → Rex → Auditor → Max                                     │
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

### 1. Multi-Pipeline Architecture

Mortgage-Lite supports three distinct pipelines, each optimized for specific workflows:

#### Pipeline Types

**Underwriting Pipeline** (6 agents)
- Purpose: Loan origination and underwriting review
- Stages: Intake → Extracting → Validating → Analyzing → Compliance → Delivering
- Agents: Iris, Rex, Val, Ana, Claire, Max

**Servicing Pipeline** (4 agents)
- Purpose: Loan servicing transfer validation
- Stages: Received → Extracting → Reconciling → Delivering
- Agents: Iris, Rex, Servo, Max

**Quality Control Pipeline** (4 agents)
- Purpose: Post-close audit and defect tracking
- Stages: Sampled → Extracting → Auditing → Delivering
- Agents: Iris, Rex, Auditor, Max

### 2. Agent Catalog

Eight specialized agents handle different aspects of processing:

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
- **Role**: Multi-engine OCR and data extraction
- **Processing**: Local
- **Functions**:
  - Document OCR with cascade fallback
  - Structured field extraction
  - Table parsing
  - Confidence scoring
- **Technology**: 
  - Vision: GLM-OCR → SecureLLM (Qwen2-VL) → Ollama (Qwen2-VL) → Tesseract
  - Field extraction: SecureLLM (Qwen 3.5) → Ollama (Qwen 3.5)
- **Output**: ExtractedField records with confidence scores

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
- **Role**: Contextual analysis using local LLM
- **Processing**: Local (privacy-safe)
- **Functions**:
  - Phonetic name mismatch detection
  - Employment gap analysis
  - Income cross-referencing
  - Large deposit investigation
  - DTI/LTV calculation
  - PII entity detection for anonymization
- **Technology**: SecureLLM → Ollama fallback (Qwen 3.5 35B)
- **Output**: Anomaly records (tier 2), PII mapping
- **Fallback**: Deterministic checks if LLMs unavailable

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
  - Generates executive summary
  - Sends Telegram notifications
  - Updates application status to completed
  - Archives processed files
- **Technology**: Template-based reporting
- **Output**: Final report, notifications sent

#### Servo (Servicing Validator Agent)
- **Role**: Servicing transfer validation
- **Processing**: Local (deterministic)
- **Functions**:
  - Principal balance reconciliation
  - Payment history gap detection
  - Escrow balance verification
  - Interest rate consistency checks
  - Insurance/tax certificate currency validation
- **Technology**: Pure Python deterministic checks
- **Output**: Transfer validation report, critical flags

#### Auditor (QC Agent)
- **Role**: Post-close quality control
- **Processing**: Local (deterministic)
- **Functions**:
  - Stale appraisal detection (>120 days)
  - Missing signature identification
  - Income calculation verification
  - Document completeness validation
  - TRID tolerance compliance
- **Technology**: Pure Python deterministic checks
- **Output**: QC audit report, defect flags

### 3. PDF Document Viewer

**Inline Document Preview**
- Embedded PDF viewer in anomaly inspector
- Page navigation and zoom controls
- Field highlighting with bounding boxes
- Multi-document tabs
- Extracted fields display

**Features**:
- Click anomaly to jump to relevant document page
- Visual field highlighting for flagged data
- Side-by-side document comparison
- Supports all PDF documents in application

### 4. Privacy Boundaries

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
- **Backend**: FastAPI (Python 3.12+)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **AI Models**: 
  - **SecureLLM** (primary) - Local inference gateway with dynamic model discovery
  - **Ollama** (fallback) - Local LLM for privacy-safe processing
  - **Claude** (Anthropic) - Cloud compliance checking (anonymized data only)
  - **GLM-OCR** - Specialized document OCR
- **Frontend**: HTMX + TailwindCSS
- **Deployment**: Docker, Kubernetes (Helm charts included)

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
