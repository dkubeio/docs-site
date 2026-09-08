# MortIQ

![MortIQ](./media/icon.svg)

**MortIQ** is an AI-powered mortgage underwriting assistant that automates document
processing, validation, and compliance checking for mortgage applications. Built with
privacy-first principles, it uses a multi-agent architecture to process mortgage packets
in minutes while keeping sensitive borrower data on your own infrastructure.

![MortIQ Command Center dashboard](./media/screenshot-1.png)

## What MortIQ does

MortIQ takes a mortgage packet — W-2s, bank statements, tax returns, pay stubs,
appraisals, and ID documents — and runs it through a pipeline of specialized AI agents
that classify, extract, validate, analyze, and compliance-check the application. It
supports three workflows:

- **Underwriting** — automate review of purchase, refinance, FHA, VA, and HELOC loans.
- **Servicing transfer** — validate data integrity when loans change servicer.
- **Quality control** — audit closed loan files for defects before delivery.

![Applications Kanban board](./media/screenshot-2.png)

## Main components

MortIQ is built around eight specialized agents that hand work off to one another:

| Agent | Role | Pipelines |
| --- | --- | --- |
| **Iris** | Document intake and classification | All |
| **Rex** | Multi-engine OCR extraction | All |
| **Val** | Deterministic validation | Underwriting |
| **Ana** | Local LLM analysis | Underwriting |
| **Claire** | Cloud-based compliance checking | Underwriting |
| **Servo** | Servicing transfer validator | Servicing |
| **Auditor** | Post-close QC auditor | Quality control |
| **Max** | Final delivery and notifications | All |

## Key features

- **Privacy-first processing** — sensitive data is handled on-premises by local LLMs,
  and PII is anonymized before any cloud service sees it. Anonymization mappings are
  ephemeral and destroyed after use.
- **Fast turnaround** — applications are processed in roughly four minutes instead of
  the industry-standard several days.
- **Real-time Kanban board** — track every application as it moves through pipeline
  stages.
- **PDF document viewer** — inline document preview with flagged fields highlighted by
  bounding box.
- **Anomaly detection** — issues are surfaced with severity classification
  (critical / warning / info).
- **Compliance checking** — applications are checked against Fannie Mae, FHA, VA, and
  Freddie Mac guidelines.
- **Audit trail** — a complete, timestamped history of every processing step.
- **Telegram notifications** — optional alerts for critical events.

## How privacy works

MortIQ separates processing into trust zones so cloud services never see real personal
information:

- **Local zone** — Iris, Rex, Val, and Ana process raw PII on local infrastructure.
- **Anonymization boundary** — data is sanitized before any cloud processing.
- **Cloud zone** — Claire receives only anonymized data for compliance analysis.
- **Deanonymization** — results are restored with real identities for final delivery.

## Tutorials

- [Getting started](./getting-started.md) — install MortIQ, load the demo data, and run
  your first application through a pipeline.

```{toctree}
:hidden:

getting-started
```
