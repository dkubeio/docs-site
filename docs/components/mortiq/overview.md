# MortIQ Overview

![MortIQ Icon](./media/mortiq-icon.svg)

**MortIQ** is an AI-powered mortgage underwriting assistant that automates document processing, validation, and compliance checking for mortgage applications. Built with privacy-first principles, it uses a multi-agent architecture to process mortgage packets efficiently while maintaining strict data security.

## Key Features

### 🤖 Eight Specialized AI Agents
- **Iris** - Document intake and classification (all pipelines)
- **Rex** - Multi-engine OCR extraction (all pipelines)
- **Val** - Deterministic validation (underwriting)
- **Ana** - Local LLM analysis (underwriting)
- **Claire** - Cloud-based compliance checking (underwriting)
- **Servo** - Servicing transfer validator (servicing)
- **Auditor** - Post-close QC auditor (quality control)
- **Max** - Final delivery and notifications (all pipelines)

### 🔒 Privacy-First Architecture
- **Local Processing**: Sensitive data processed on-premises with local LLMs
- **Anonymization**: PII automatically anonymized before cloud processing
- **Ephemeral Mappings**: Anonymization mappings destroyed after use
- **Zero PII Exposure**: Cloud services never see real personal information

### ⚡ Performance
- **4x Faster**: Process applications in ~4 minutes vs industry standard of 4 days
- **Cost Efficient**: 60% reduction in cloud AI costs through intelligent routing
- **Parallel Processing**: Multi-document concurrent extraction
- **Shift-Left Validation**: Catch errors early with deterministic checks

### 📊 Comprehensive Features
- **Multi-Pipeline Support**: Underwriting, Servicing Transfer, and Quality Control
- **Real-time Kanban Board**: Track applications across pipeline stages
- **PDF Document Viewer**: Inline document preview with field highlighting
- **Anomaly Detection**: Severity classification (critical/warning/info)
- **Compliance Checking**: Fannie Mae, FHA, VA, and Freddie Mac guidelines
- **Executive Summary**: Cross-document synthesis with AI
- **Audit Trail**: Complete processing history with timestamps
- **Telegram Notifications**: Critical event alerts

## Use Cases

### 1. Mortgage Underwriting
Automate the review of mortgage applications including:
- Purchase loans
- Refinance applications
- FHA loans
- VA loans
- HELOC applications

### 2. Loan Servicing Transfer
Validate data integrity during loan servicing transfers:
- Principal balance reconciliation
- Payment history completeness
- Escrow balance verification
- Interest rate consistency
- Insurance and tax certificate currency

### 3. Post-Close Quality Control
Audit closed loan files for defects:
- Missing signatures detection
- Stale appraisal checks (>120 days)
- Income calculation verification
- Document completeness validation
- TRID tolerance compliance

### Document Processing
Extract and validate data from:
- W-2 forms
- 1099 forms
- Bank statements
- Tax returns
- Pay stubs
- Appraisals
- ID documents

### Compliance Verification
Automatically check applications against:
- Debt-to-Income (DTI) ratios
- Loan-to-Value (LTV) ratios
- Credit score requirements
- Required documentation
- Regulatory guidelines

## Architecture Highlights

### Underwriting Pipeline
```
UPLOAD → Iris → Rex → Val → Ana → [ANONYMIZE] → Claire → [DEANONYMIZE] → Max → DONE
         ↓       ↓      ↓      ↓                   ↓                         ↓
      Classify  OCR   Validate Analyze          Comply                    Deliver
```

### Servicing Pipeline
```
RECEIVED → Iris → Rex → Servo → Max → TRANSFERRED
           ↓       ↓      ↓        ↓
        Classify  OCR  Reconcile Deliver
```

### Quality Control Pipeline
```
SAMPLED → Iris → Rex → Auditor → Max → CLEARED/DEFECT
          ↓       ↓      ↓          ↓
       Classify  OCR   Audit     Deliver
```

### Privacy Boundaries
- **Local Zone**: Iris, Rex, Val, Ana process raw PII on local infrastructure
- **Anonymization Boundary**: Data sanitized before cloud processing
- **Cloud Zone**: Claire receives only anonymized data
- **Deanonymization**: Results restored with real identities for delivery

## Technology Stack

- **Backend**: FastAPI (Python 3.12+)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **AI Models**: 
  - Claude (Anthropic) for compliance
  - Qwen 3.5 (local) for analysis
  - GLM-OCR for document extraction
- **Frontend**: HTMX + TailwindCSS
- **Deployment**: Docker, Kubernetes (Helm charts included)

## Quick Start

See [Getting Started](./getting-started.md) for installation and setup instructions.

## Documentation

- [Getting Started](./getting-started.md) - Installation and first steps
- [Architecture](./architecture.md) - System design and components
- [API Reference](./api-reference.md) - REST API documentation
- [Deployment](./deployment.md) - Production deployment guide

## Support

For issues, questions, or contributions, please refer to the project repository.

## License

See LICENSE file in the repository root.
