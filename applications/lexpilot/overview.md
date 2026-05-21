# Overview

> **Quick Summary:** LexPilot is an AI-powered legal document processing platform that automates contract review, compliance checking, and risk analysis for corporate transactions.

---

## 1.1 What is LexPilot?

**LexPilot** is an intelligent legal automation platform designed to streamline the review and analysis of corporate legal documents. Built specifically for venture capital financings, M&A transactions, company formations, and securities offerings, LexPilot combines AI-powered document processing with deterministic compliance checking to deliver fast, accurate, and consistent legal review.

### Mission Statement

Our mission is to **democratize access to sophisticated legal technology** by providing law firms, corporate legal departments, and investment funds with enterprise-grade document automation that can be deployed privately, securely, and cost-effectively.

### Core Value Proposition

| Traditional Manual Review | LexPilot Automated Review |
|--------------------------|---------------------------|
| 8-12 hours per transaction | 30 minutes per transaction |
| $2,000-$3,000 in attorney time | $50-$100 in compute costs |
| 85-90% consistency | 95%+ consistency |
| Linear scalability | Exponential scalability |
| Variable quality (fatigue, experience) | Consistent quality (AI + rules) |
| No audit trail | Complete audit trail |

### Key Capabilities

- **🔍 Intelligent Document Classification** - Automatically identifies document types (term sheets, stock purchase agreements, board resolutions, etc.)
- **📄 Advanced OCR & Extraction** - Extracts text from scanned PDFs and parses structured fields (parties, dates, amounts, terms)
- **✅ Deterministic Validation** - Checks for entity name consistency, amount mismatches, date conflicts, missing documents
- **🧠 AI-Powered Analysis** - Deep contract review identifying risks, obligations, and unusual terms
- **⚖️ Compliance Checking** - Validates against 50+ regulatory rules (CA Corp Code, SEC Reg D, Delaware law, etc.)
- **📊 Automated Reporting** - Generates comprehensive PDF reports with findings and recommendations
- **📱 Real-Time Notifications** - Telegram/Slack alerts for pipeline completion and critical issues

---

## 1.2 Why LexPilot?

### The Problem: Manual Legal Review Bottlenecks

Corporate legal teams face mounting pressure:

1. **Volume Overload** - Increasing deal flow without proportional headcount growth
2. **Time Constraints** - Tight closing timelines demand faster turnaround
3. **Cost Pressure** - Clients push back on high legal fees for routine work
4. **Consistency Issues** - Junior associates produce variable quality work
5. **Risk Exposure** - Manual review misses critical issues due to fatigue or inexperience
6. **No Scalability** - Can't handle 10x deal volume without 10x headcount

### The Solution: AI-Powered Automation

LexPilot addresses these challenges through:

#### 1. **Speed** ⚡
- Process entire deal packages in minutes, not days
- Parallel document processing across multiple agents
- Real-time progress tracking and notifications

#### 2. **Accuracy** 🎯
- 95%+ field extraction accuracy with multi-provider AI
- Deterministic validation catches 100% of rule violations
- Continuous learning from corrections

#### 3. **Consistency** 📏
- Same rules applied to every document, every time
- No variation based on reviewer experience or fatigue
- Standardized output format and quality

#### 4. **Cost-Effectiveness** 💰
- 95% reduction in attorney time on routine review
- Self-hosted option eliminates SaaS fees
- Pay only for AI compute (as low as $0 with local models)

#### 5. **Scalability** 📈
- Handle 10x deal volume with same infrastructure
- Horizontal scaling for peak periods
- No hiring or training required

#### 6. **Security & Privacy** 🔒
- 100% on-premises deployment option
- No data sent to cloud (air-gapped mode)
- Full control over AI models and data

### Key Differentiators

#### 🔒 **Private & Secure First**
Unlike cloud-only competitors, LexPilot offers:
- **Full on-premises deployment** - All data stays in your infrastructure
- **Air-gapped operation** - No internet connection required
- **Bring your own AI** - Use local Ollama models or your own fine-tuned models
- **Zero vendor lock-in** - Open source core, standard formats

#### 🌐 **Hybrid Flexibility**
Best of both worlds:
- **Local data storage** - Sensitive documents never leave your servers
- **Cloud AI processing** - Leverage powerful cloud models when needed
- **Automatic anonymization** - PII replaced with tokens before cloud processing
- **Cost optimization** - Use expensive cloud AI only when necessary

#### 🔧 **Open & Extensible**
Built for customization:
- **Open source core** - Full visibility into processing logic
- **Plugin architecture** - Add custom agents and compliance rules
- **API-first design** - Integrate with existing workflows
- **Multi-provider AI** - Switch between Ollama, OpenRouter, Claude, Azure OpenAI

#### 💡 **Purpose-Built for Corporate Law**
Not a generic contract tool:
- **Transaction-specific workflows** - VC, M&A, formation, securities
- **Jurisdiction-aware** - CA, DE, NY, TX, Federal rules
- **Matter-centric** - Organize by deal, not individual documents
- **Compliance-focused** - 50+ built-in regulatory checks

---

## 1.3 Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        LexPilot Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Web UI     │  │  REST API    │  │   Webhooks   │     │
│  │  (HTMX +     │  │  (FastAPI)   │  │  (Telegram,  │     │
│  │  Tailwind)   │  │              │  │   Slack)     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│  ┌─────────────────────────┴─────────────────────────┐     │
│  │              Agent Orchestration Layer             │     │
│  │  (Async task queue, SSE streaming, state mgmt)    │     │
│  └─────────────────────────┬─────────────────────────┘     │
│                            │                                 │
│  ┌─────────────────────────┴─────────────────────────┐     │
│  │              Five-Agent Pipeline                   │     │
│  │                                                     │     │
│  │  Lex → Petra → Gavel → Reese → Portia            │     │
│  │  (Classify) (Extract) (Validate) (Analyze) (Comply)│    │
│  └─────────────────────────┬─────────────────────────┘     │
│                            │                                 │
│  ┌─────────────────────────┴─────────────────────────┐     │
│  │              Service Layer                         │     │
│  │                                                     │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐          │     │
│  │  │   OCR    │ │    AI    │ │Compliance│          │     │
│  │  │ Service  │ │ Service  │ │  Engine  │          │     │
│  │  └──────────┘ └──────────┘ └──────────┘          │     │
│  └─────────────────────────┬─────────────────────────┘     │
│                            │                                 │
│  ┌─────────────────────────┴─────────────────────────┐     │
│  │              Data Layer                            │     │
│  │                                                     │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐          │     │
│  │  │ SQLite/  │ │  File    │ │ Settings │          │     │
│  │  │PostgreSQL│ │ Storage  │ │   DB     │          │     │
│  │  └──────────┘ └──────────┘ └──────────┘          │     │
│  └───────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

External Integrations:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  OpenRouter  │  │    Ollama    │  │    Claude    │
│  (Cloud AI)  │  │  (Local AI)  │  │  (Fallback)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Agent Pipeline Flow

```
Document Upload
      │
      ▼
┌─────────────┐
│    LEX      │  Intake & Classification
│ (No AI)     │  • Pattern matching on filename
│ ~0.5s       │  • Assigns document type
└─────┬───────┘  • 95%+ accuracy
      │
      ▼
┌─────────────┐
│   PETRA     │  OCR & Field Extraction
│ (AI: Vision │  • Extracts text from scanned PDFs
│  + Text)    │  • Parses structured fields
│ ~20s        │  • Multi-provider support
└─────┬───────┘  • 88% field accuracy
      │
      ▼
┌─────────────┐
│   GAVEL     │  Deterministic Validation
│ (No AI)     │  • Entity name consistency
│ ~2s         │  • Amount matching
└─────┬───────┘  • Date conflict detection
      │          • Missing document checks
      ▼
┌─────────────┐
│   REESE     │  Contract Analysis
│ (AI: Text)  │  • Risk identification
│ ~25s        │  • Obligation extraction
└─────┬───────┘  • Unusual term flagging
      │
      ▼
┌─────────────┐
│   PORTIA    │  Compliance Checking
│ (AI: Text)  │  • 50+ regulatory rules
│ ~20s        │  • Jurisdiction-specific
└─────┬───────┘  • Scoring and reporting
      │
      ▼
  Completed
  (Report Generated)
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTMX + TailwindCSS | Reactive UI without heavy JavaScript |
| **Backend** | FastAPI (Python 3.11) | High-performance async API |
| **Database** | SQLite / PostgreSQL | Structured data storage |
| **File Storage** | Local filesystem | Document and upload storage |
| **AI Providers** | OpenRouter, Ollama, Claude | Multi-provider AI processing |
| **OCR** | OpenRouter Vision, GLM-OCR, Tesseract | Text extraction from scans |
| **Deployment** | Docker + Kubernetes | Container orchestration |
| **Notifications** | Telegram, Slack (roadmap) | Real-time alerts |
| **Monitoring** | Structured logging | Observability |

### Deployment Models

#### 1. **Private Deployment** (Recommended for Enterprises)
```
┌─────────────────────────────────────┐
│     Your Infrastructure             │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      LexPilot Platform       │  │
│  │  (All components on-prem)    │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Ollama (Local AI)       │  │
│  │  (Your own LLM models)       │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Database & Storage      │  │
│  │  (Your own infrastructure)   │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘

✅ 100% data control
✅ Air-gapped option
✅ No cloud dependencies
✅ Compliance-ready
```

#### 2. **Hybrid Deployment** (Best of Both Worlds)
```
┌─────────────────────────────────────┐
│     Your Infrastructure             │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      LexPilot Platform       │  │
│  │  (Core + Anonymization)      │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────┴───────────────────┐  │
│  │   Anonymization Boundary     │  │
│  │  (PII → Tokens)              │  │
│  └──────────┬───────────────────┘  │
│             │                       │
└─────────────┼───────────────────────┘
              │ Anonymized Data
              ▼
┌─────────────────────────────────────┐
│         Cloud AI Providers          │
│  (OpenRouter, Claude, Azure)        │
│  (Processes only anonymized data)   │
└─────────────────────────────────────┘

✅ Sensitive data stays local
✅ Leverage powerful cloud AI
✅ Cost-optimized
✅ Flexible scaling
```

#### 3. **Cloud Deployment** (Fastest Setup)
```
┌─────────────────────────────────────┐
│      Cloud Provider (AWS/GCP)       │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      LexPilot Platform       │  │
│  │  (Fully managed)             │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Cloud AI Services       │  │
│  │  (OpenRouter, Claude)        │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘

✅ Fastest deployment
✅ Minimal ops overhead
✅ Auto-scaling
⚠️ Data in cloud
```

---

## 1.4 Quick Start (5-Minute Guide)

Get LexPilot running and process your first deal in 5 minutes.

### Prerequisites

- Docker installed
- 8GB RAM minimum
- 20GB disk space

### Step 1: Pull and Run Docker Image

```bash
# Pull the latest LexPilot image
docker pull ghcr.io/dkubeio/law-lite:latest

# Run LexPilot
docker run -d \
  -p 5310:5310 \
  -v $(pwd)/lexpilot-data:/app/uploads \
  -v $(pwd)/lexpilot-db:/app \
  --name lexpilot \
  ghcr.io/dkubeio/law-lite:latest

# Check if running
docker ps | grep lexpilot
```

### Step 2: Access the UI

Open your browser to: **http://localhost:5310**

You should see the LexPilot dashboard:

```
┌─────────────────────────────────────────────────┐
│  ⚖️  LEXPILOT                    [Settings]    │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Dashboard                                   │
│                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────┐│
│  │   Matters   │ │  Documents  │ │  Issues   ││
│  │      0      │ │      0      │ │     0     ││
│  └─────────────┘ └─────────────┘ └───────────┘│
│                                                 │
│  Recent Activity                                │
│  (No matters yet)                               │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Step 3: Configure AI Provider (Optional)

For best results, configure an AI provider:

**Option A: Use OpenRouter (Cloud, Free Tier)**

1. Go to **Settings** tab
2. Set **AI Provider** to `OpenRouter`
3. Enter **OpenRouter API Key**: `sk-or-v1-...` (get free key at openrouter.ai)
4. Set **OpenRouter Model**: `google/gemma-4-31b-it:free`
5. Click **Save Settings**

**Option B: Use Ollama (Local, Private)**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull qwen2.5:14b

# LexPilot will auto-detect Ollama at localhost:11434
```

### Step 4: Create Your First Matter

1. Click **Matters** in sidebar
2. Click **+ New Matter**
3. Fill in the form:
   ```
   Matter Name: Acme Corp Series A
   Client Name: Acme Corp
   Matter Type: vc (Venture Capital)
   Deal Value: 5000000
   Jurisdiction: CA (California)
   ```
4. Click **Create Matter**

### Step 5: Upload Documents

1. Click **Upload** in sidebar
2. Select your matter: `Acme Corp Series A`
3. Drag and drop PDF files:
   - `TermSheet_AcmeCorp.pdf`
   - `StockPurchaseAgreement.pdf`
   - `BoardResolution.pdf`
4. Click **Upload**

### Step 6: Watch the Pipeline Process

1. Click **Agents** in sidebar
2. Watch real-time progress:
   ```
   ┌─────────────────────────────────────────┐
   │  Agent Pipeline - Acme Corp Series A    │
   ├─────────────────────────────────────────┤
   │  ✅ Lex       Classified 3 documents    │
   │  🔄 Petra     Extracting fields... 60%  │
   │  ⏳ Gavel     Waiting...                │
   │  ⏳ Reese     Waiting...                │
   │  ⏳ Portia    Waiting...                │
   └─────────────────────────────────────────┘
   ```

Processing typically takes **1-2 minutes** for 3-5 documents.

### Step 7: Review Results

Once complete, navigate to your matter:

1. Click **Matters** → `Acme Corp Series A`
2. Review the summary:
   ```
   Status: ✅ Completed
   
   Documents: 3 processed
   Fields Extracted: 12
   Issues Found: 2 (1 critical, 1 warning)
   Compliance: 85% (17/20 rules passed)
   ```

3. Click **Issues** tab to see flagged items:
   ```
   🚨 CRITICAL: Purchase price mismatch
      Term Sheet: $5,000,000
      SPA: $5,500,000
      
   ⚠️  WARNING: Missing accredited investor questionnaire
   ```

4. Click **Compliance** tab to see rule checks:
   ```
   ✅ CA Corp Code - Agent for service (PASSED)
   ✅ SEC Reg D - Form D filing required (PASSED)
   ❌ CA 25102(f) - Max 35 investors (FAILED)
   ```

### Step 8: Generate Report

1. Click **Reports** tab
2. Click **Generate PDF Report**
3. Download comprehensive deal summary

**Congratulations!** 🎉 You've processed your first deal with LexPilot.

---

## What's Next?

Now that you've seen LexPilot in action, explore:

- **[Features →](features.md)** - Deep dive into all capabilities
- **[User Guide →](user-guide.md)** - Detailed usage instructions
- **[Use Cases →](use-cases.md)** - Transaction-specific workflows

---

## Getting Help

- 📖 **Documentation**: You're reading it!
- 💬 **Community**: [GitHub Discussions](https://github.com/dkubeio/law-lite/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/dkubeio/law-lite/issues)
- 📧 **Email**: support@lexpilot.ai
- 💼 **Enterprise**: enterprise@lexpilot.ai

---

**Last Updated:** April 2026 | **Version:** 1.1.8
