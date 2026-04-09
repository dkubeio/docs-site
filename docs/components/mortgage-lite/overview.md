# Mortgage-Lite Overview

![Mortgage-Lite Icon](./media/mortgage-lite-icon.svg)

**Mortgage-Lite** is an AI-powered mortgage underwriting assistant that automates document processing, validation, and compliance checking for mortgage applications. Built with privacy-first principles, it uses a multi-agent architecture to process mortgage packets efficiently while maintaining strict data security.

## Key Features

### 🤖 Six Specialized AI Agents
- **Iris** - Document intake and classification
- **Rex** - Multi-engine OCR extraction
- **Val** - Deterministic validation (zero AI cost)
- **Ana** - Local LLM analysis (privacy-safe)
- **Claire** - Cloud-based compliance checking (anonymized data only)
- **Max** - Final delivery and notifications

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
- Real-time kanban board for application tracking
- Anomaly detection with severity classification
- Compliance checking against Fannie Mae, FHA, VA, and Freddie Mac guidelines
- Executive summary generation with cross-document synthesis
- Audit trail with complete processing history
- Telegram notifications for critical events

## Use Cases

### Mortgage Underwriting
Automate the review of mortgage applications including:
- Purchase loans
- Refinance applications
- FHA loans
- VA loans
- HELOC applications

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

```
UPLOAD → Iris → Rex → Val → Ana → [ANONYMIZE] → Claire → [DEANONYMIZE] → Max → DONE
         ↓       ↓      ↓      ↓                   ↓                         ↓
      Classify  OCR   Validate Analyze          Comply                    Deliver
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
