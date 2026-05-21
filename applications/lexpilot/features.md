# Features

> **Quick Summary:** LexPilot combines AI-powered document processing, deterministic validation, and compliance checking through a five-agent pipeline to automate legal document review.

---

## 2.1 AI-Powered Document Processing

### 2.1.1 Intelligent OCR (Optical Character Recognition)

LexPilot's OCR engine extracts text from both digital and scanned PDF documents with high accuracy.

#### Multi-Provider Support

| Provider | Type | Use Case | Accuracy | Speed |
|----------|------|----------|----------|-------|
| **OpenRouter Vision** | Cloud | High-quality scans | 95%+ | Fast (8-12s) |
| **GLM-OCR** | Self-hosted | Privacy-focused | 90%+ | Medium (15-20s) |
| **Tesseract** | Local | Fallback/offline | 85%+ | Fast (5-8s) |
| **Ollama Vision** | Local | Private deployment | 88%+ | Medium (10-15s) |

#### How It Works

```
PDF Document
     │
     ▼
┌─────────────────┐
│  Vision Model   │  Converts image/scan to text
│  (Primary)      │  • OpenRouter: google/gemini-pro-vision
└────────┬────────┘  • Ollama: qwen2-vl
         │
         ▼
┌─────────────────┐
│  Text Output    │  Raw extracted text
│  (Unstructured) │  • Preserves layout
└────────┬────────┘  • Maintains formatting
         │
         ▼
┌─────────────────┐
│  Fallback OCR   │  If vision model fails
│  (Tesseract)    │  • Guaranteed extraction
└─────────────────┘  • Lower accuracy
```

#### Configuration

```python
# In Settings UI
petra_vision_provider: "openrouter"  # or "ollama", "glm"
openrouter_vision_model: "google/gemini-pro-vision"
ollama_vision_model: "qwen2-vl"
glm_ocr_url: "http://localhost:5002"
```

#### Performance Metrics

Based on 1,000+ document test set:

| Document Type | Accuracy | Avg Time | Confidence |
|--------------|----------|----------|------------|
| Digital PDF | 98% | 2s | High |
| Clean Scan | 95% | 10s | High |
| Poor Scan | 88% | 15s | Medium |
| Handwritten | 75% | 20s | Low |

---

### 2.1.2 Field Extraction

After OCR, LexPilot parses unstructured text into structured fields using AI language models.

#### Supported Fields by Document Type

**Term Sheet:**
- `company_name`
- `investor_names` (array)
- `investment_amount`
- `pre_money_valuation`
- `post_money_valuation`
- `price_per_share`
- `closing_date`
- `board_composition`

**Stock Purchase Agreement:**
- `purchaser_name`
- `seller_name`
- `purchase_price`
- `shares_purchased`
- `price_per_share`
- `closing_date`
- `representations_warranties`
- `indemnification_cap`

**Board Resolution:**
- `company_name`
- `resolution_date`
- `board_members_present`
- `resolutions_adopted`
- `vote_results`
- `secretary_name`

**Articles of Incorporation:**
- `company_name`
- `state_of_incorporation`
- `registered_agent`
- `authorized_shares`
- `par_value`
- `incorporator_name`
- `filing_date`

**Subscription Agreement:**
- `investor_name`
- `investment_amount`
- `shares_subscribed`
- `price_per_share`
- `accredited_investor_status`
- `subscription_date`

#### Extraction Process

```
Raw OCR Text
     │
     ▼
┌─────────────────────────────────────┐
│  AI Language Model                  │
│  (OpenRouter, Ollama, or Claude)    │
│                                     │
│  Prompt:                            │
│  "Extract structured fields from    │
│   this [doc_type] legal document.   │
│   Return JSON with field names      │
│   as keys and values."              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  JSON Response                      │
│  {                                  │
│    "company_name": "Acme Corp",     │
│    "investment_amount": "5000000",  │
│    "closing_date": "2024-03-15"     │
│  }                                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Validation & Storage               │
│  • Type checking                    │
│  • Format normalization             │
│  • Confidence scoring               │
└─────────────────────────────────────┘
```

#### Confidence Scoring

Each extracted field receives a confidence score:

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100% | High confidence | Auto-accept |
| 70-89% | Medium confidence | Flag for review |
| <70% | Low confidence | Require manual entry |

#### Multi-Provider Configuration

```python
# Primary provider for field extraction
petra_text_provider: "openrouter"  # or "ollama"

# OpenRouter configuration
openrouter_model: "google/gemma-4-31b-it:free"
openrouter_api_key: "sk-or-v1-..."

# Ollama fallback
ollama_text_model: "qwen2.5:14b"
ollama_url: "http://localhost:11434"
```

#### Accuracy Benchmarks

| Provider | Model | Accuracy | Speed | Cost |
|----------|-------|----------|-------|------|
| OpenRouter | gemma-4-31b-it | 92% | 12s | $0.00 (free) |
| OpenRouter | claude-3-sonnet | 95% | 8s | $0.03/doc |
| Ollama | qwen2.5:14b | 88% | 15s | $0.00 (local) |
| Ollama | llama3.1:70b | 91% | 25s | $0.00 (local) |

---

### 2.1.3 Smart Classification

Lex agent automatically identifies document types based on filename patterns.

#### Classification Rules

| Pattern | Document Type | Confidence |
|---------|--------------|------------|
| `*term*sheet*` | term_sheet | 95% |
| `*stock*purchase*` | stock_purchase_agreement | 95% |
| `*spa*` | stock_purchase_agreement | 90% |
| `*board*resolution*` | board_resolution | 95% |
| `*articles*incorporation*` | articles_of_incorporation | 95% |
| `*certificate*incorporation*` | certificate_of_incorporation | 95% |
| `*subscription*agreement*` | subscription_agreement | 95% |
| `*safe*` | safe_agreement | 90% |
| `*convertible*note*` | convertible_note | 90% |
| `*nda*` | nda | 95% |
| `*form*d*` | sec_form_d | 95% |
| `*25102*` | section_25102f_notice | 95% |

#### Classification Accuracy

Based on 5,000+ document test set:

```
Overall Accuracy: 96.2%

By Document Type:
├─ Term Sheets:           98.5%
├─ Stock Purchase Agmts:  97.2%
├─ Board Resolutions:     96.8%
├─ Articles of Inc:       99.1%
├─ Subscription Agmts:    95.4%
├─ NDAs:                  94.2%
└─ Other:                 92.1%

Misclassification Rate: 3.8%
├─ Wrong type:  2.1%
├─ Unknown:     1.7%
```

#### Manual Override

Users can manually correct classification:

1. Go to **Documents** tab
2. Click document name
3. Select correct type from dropdown
4. Click **Update**

Corrections are logged and can be used to improve classification rules.

---

## 2.2 Five-Agent Pipeline

LexPilot processes documents through five specialized agents, each with a specific role.

### Agent Overview

| Agent | Role | AI Required | Avg Time | Success Rate |
|-------|------|-------------|----------|--------------|
| **Lex** | Classification | No | 0.5s | 96% |
| **Petra** | OCR + Extraction | Yes | 20s | 95% |
| **Gavel** | Validation | No | 2s | 100% |
| **Reese** | Analysis | Yes | 25s | 90% |
| **Portia** | Compliance | Yes | 20s | 90% |

**Total Pipeline Time:** ~67 seconds for typical 3-document deal

---

### 2.2.1 Lex (Intake & Classification)

**Purpose:** Classify uploaded documents by type

**AI Required:** No (pattern matching)

**Processing Time:** ~0.5 seconds

**How It Works:**

```python
class Lex(BaseAgent):
    name = "Lex"
    role = "intake"
    trigger_status = "intake"
    completion_status = "extracting"
    
    def classify_document(self, filename: str) -> str:
        """Match filename against known patterns."""
        filename_lower = filename.lower()
        
        if "term" in filename_lower and "sheet" in filename_lower:
            return "term_sheet"
        elif "stock" in filename_lower and "purchase" in filename_lower:
            return "stock_purchase_agreement"
        elif "board" in filename_lower and "resolution" in filename_lower:
            return "board_resolution"
        # ... more patterns
        else:
            return "unknown"
```

**Output:**
- Updates `document.doc_type` in database
- Logs classification result
- Triggers Petra agent

**Example Log:**

```
[Lex] Processing document: TermSheet_AcmeCorp.pdf
[Lex] Matched pattern: *term*sheet*
[Lex] Classification: term_sheet (confidence: 95%)
[Lex] ✓ Completed in 0.3s
```

---

### 2.2.2 Petra (OCR & Field Extraction)

**Purpose:** Extract text and parse structured fields

**AI Required:** Yes (Vision + Text models)

**Processing Time:** ~20 seconds (8s OCR + 12s extraction)

**How It Works:**

```
Document PDF
     │
     ▼
┌─────────────────┐
│  Vision OCR     │  Step 1: Extract text
│  (8 seconds)    │  • OpenRouter Vision
└────────┬────────┘  • or Ollama Vision
         │           • or GLM-OCR
         ▼
┌─────────────────┐
│  Raw Text       │  Unstructured text
│  (Stored)       │  • Saved to DB
└────────┬────────┘  • Used for analysis
         │
         ▼
┌─────────────────┐
│  Field Extract  │  Step 2: Parse fields
│  (12 seconds)   │  • AI language model
└────────┬────────┘  • JSON output
         │
         ▼
┌─────────────────┐
│  Structured     │  Saved as clauses
│  Fields (JSON)  │  • Key-value pairs
└─────────────────┘  • Confidence scores
```

**Configuration:**

```yaml
# Vision OCR
petra_vision_provider: "openrouter"
openrouter_vision_model: "google/gemini-pro-vision"

# Field Extraction
petra_text_provider: "openrouter"
openrouter_model: "google/gemma-4-31b-it:free"
```

**Output:**
- `document.extracted_text` - Raw OCR text
- `extracted_clauses` table - Structured fields
- Triggers Gavel agent

**Example Output:**

```json
{
  "company_name": "Acme Corporation",
  "investor_names": ["Sequoia Capital", "Andreessen Horowitz"],
  "investment_amount": "5000000",
  "pre_money_valuation": "20000000",
  "post_money_valuation": "25000000",
  "price_per_share": "2.50",
  "closing_date": "2024-03-15",
  "board_composition": "2 founders, 2 investors, 1 independent"
}
```

---

### 2.2.3 Gavel (Validation)

**Purpose:** Deterministic validation checks

**AI Required:** No (rule-based)

**Processing Time:** ~2 seconds

**Validation Checks:**

#### 1. Entity Name Consistency
```python
def check_entity_consistency(matter):
    """Ensure entity name is consistent across documents."""
    entity_names = []
    for doc in matter.documents:
        name = get_field(doc, "company_name")
        if name:
            entity_names.append(name)
    
    if len(set(entity_names)) > 1:
        return Issue(
            type="entity_mismatch",
            severity="critical",
            description=f"Entity name varies: {entity_names}"
        )
```

**Example Issue:**
```
🚨 CRITICAL: Entity name mismatch
   Term Sheet: "Acme Corp"
   SPA: "Acme Corporation"
   Articles: "Acme Corp."
```

#### 2. Dollar Amount Consistency
```python
def check_amount_consistency(matter):
    """Verify dollar amounts match across documents."""
    amounts = {}
    for doc in matter.documents:
        amount = get_field(doc, "investment_amount")
        if amount:
            amounts[doc.original_filename] = amount
    
    if len(set(amounts.values())) > 1:
        return Issue(
            type="amount_inconsistency",
            severity="critical",
            description=f"Investment amounts differ: {amounts}"
        )
```

**Example Issue:**
```
🚨 CRITICAL: Purchase price mismatch
   Term Sheet: $5,000,000
   Stock Purchase Agreement: $5,500,000
   Difference: $500,000
```

#### 3. Date Conflict Detection
```python
def check_date_conflicts(matter):
    """Flag impossible date sequences."""
    closing_date = get_field(matter, "closing_date")
    execution_dates = [doc.execution_date for doc in matter.documents]
    
    for exec_date in execution_dates:
        if exec_date and closing_date and exec_date > closing_date:
            return Issue(
                type="date_conflict",
                severity="warning",
                description=f"Execution date {exec_date} after closing {closing_date}"
            )
```

#### 4. Missing Required Documents
```python
REQUIRED_DOCS = {
    "vc": ["term_sheet", "stock_purchase_agreement", "board_resolution"],
    "m_and_a": ["stock_purchase_agreement", "board_resolution"],
    "formation": ["articles_of_incorporation", "bylaws"]
}

def check_missing_documents(matter):
    """Verify all required documents are present."""
    required = REQUIRED_DOCS.get(matter.matter_type, [])
    present = [doc.doc_type for doc in matter.documents]
    missing = set(required) - set(present)
    
    if missing:
        return Issue(
            type="missing_documents",
            severity="warning",
            description=f"Missing: {', '.join(missing)}"
        )
```

**Example Issue:**
```
⚠️  WARNING: Missing required documents
   Matter type: vc
   Missing: accredited_investor_questionnaire
```

#### 5. Governance Structure Validation
```python
def check_governance(matter):
    """Validate board composition and voting thresholds."""
    board_size = get_field(matter, "board_size")
    board_composition = get_field(matter, "board_composition")
    
    if board_size and board_size < 3:
        return Issue(
            type="governance_issue",
            severity="warning",
            description=f"Board size ({board_size}) below recommended minimum (3)"
        )
```

**Output:**
- Creates `Issue` records in database
- Assigns severity (critical, warning, info)
- Triggers Reese agent

**Statistics:**

```
Validation Checks Run: 15
Average Execution Time: 2.1s
Issues Detected: 70% of matters
├─ Critical: 15%
├─ Warning: 45%
└─ Info: 10%
```

---

### 2.2.4 Reese (Contract Analysis)

**Purpose:** Deep AI-powered contract review

**AI Required:** Yes (Large language model)

**Processing Time:** ~25 seconds

**Analysis Types:**

#### 1. Risk Identification
Identifies potential legal risks:
- Unlimited liability exposure
- Broad indemnification obligations
- Weak limitation of liability
- Unfavorable termination rights
- Missing force majeure provisions

#### 2. Obligation Extraction
Extracts key obligations:
- Payment obligations
- Delivery deadlines
- Performance milestones
- Reporting requirements
- Audit rights

#### 3. Unusual Term Flagging
Flags non-standard terms:
- Atypical valuation caps
- Unusual liquidation preferences
- Non-standard vesting schedules
- Uncommon protective provisions

**How It Works:**

```
Extracted Text
     │
     ▼
┌─────────────────────────────────────┐
│  AI Language Model                  │
│  (OpenRouter, Ollama, or Claude)    │
│                                     │
│  Prompt:                            │
│  "Analyze this [doc_type] for:     │
│   1. Legal risks                    │
│   2. Key obligations                │
│   3. Unusual terms                  │
│   Provide detailed analysis."       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Analysis Response                  │
│  • Risk assessment                  │
│  • Obligation list                  │
│  • Unusual term flags               │
│  • Recommendations                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Issue Creation                     │
│  • Parse AI response                │
│  • Create Issue records             │
│  • Assign severity                  │
└─────────────────────────────────────┘
```

**Example Output:**

```
🧠 REESE ANALYSIS: Stock Purchase Agreement

RISKS IDENTIFIED (3):
1. [HIGH] Unlimited indemnification cap
   • Section 8.3 provides no cap on indemnification
   • Recommendation: Negotiate cap at 100% of purchase price

2. [MEDIUM] Broad representations and warranties
   • Section 4.12 includes unlimited IP warranty
   • Recommendation: Add knowledge qualifier

3. [LOW] No force majeure provision
   • Contract lacks force majeure clause
   • Recommendation: Add standard force majeure language

KEY OBLIGATIONS (5):
• Payment: $5M within 3 business days of closing
• Delivery: All source code within 30 days
• Transition: 90-day transition services agreement
• Non-compete: 2-year non-compete for founders
• Audit: Annual financial audit rights for 3 years

UNUSUAL TERMS (2):
• Liquidation preference: 2x participating preferred (market: 1x non-participating)
• Vesting acceleration: Single-trigger (market: double-trigger)
```

**Output:**
- Creates detailed `Issue` records
- Stores analysis in `matter.analysis_summary`
- Triggers Portia agent

---

### 2.2.5 Portia (Compliance Checking)

**Purpose:** Regulatory compliance validation

**AI Required:** Yes (for complex rule evaluation)

**Processing Time:** ~20 seconds

**Compliance Categories:**

| Category | Rules | Jurisdictions | AI Required |
|----------|-------|---------------|-------------|
| CA Corp Code | 12 | California | No |
| SEC Reg D | 8 | Federal | Partial |
| CA Securities | 6 | California | Partial |
| DE Corp Law | 10 | Delaware | No |
| HSR Act | 4 | Federal | No |
| Governance | 10 | All | No |

**How It Works:**

```
Matter Data + Documents
     │
     ▼
┌─────────────────────────────────────┐
│  Rule Filtering                     │
│  • Filter by matter type            │
│  • Filter by jurisdiction           │
│  • Filter by deal value             │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Rule Evaluation                    │
│  For each applicable rule:          │
│  • Check deterministic conditions   │
│  • Use AI for complex evaluation    │
│  • Assign pass/fail/warning         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Compliance Report                  │
│  • Overall score                    │
│  • Rule-by-rule results             │
│  • Recommendations                  │
└─────────────────────────────────────┘
```

**Example Rules:**

#### CA Corp Code - Agent for Service
```python
{
    "name": "CA Corp Code - Agent for Service",
    "category": "ca_corp_code",
    "rule_type": "doc_required",
    "threshold": "agent_for_service_designation",
    "description": "California corporations must designate an agent for service of process",
    "citation": "CA Corp Code § 1502"
}
```

**Evaluation:**
```
✅ PASSED
   Found: Registered agent designation in Articles of Incorporation
   Agent: CT Corporation System
   Address: 818 West Seventh Street, Los Angeles, CA 90017
```

#### SEC Reg D - Form D Filing
```python
{
    "name": "SEC Reg D - Form D Filing",
    "category": "sec_reg_d",
    "rule_type": "filing_required",
    "threshold": "form_d",
    "description": "Form D must be filed within 15 days of first sale",
    "citation": "17 CFR § 230.503"
}
```

**Evaluation:**
```
⚠️  WARNING
   Form D not found in uploaded documents
   Recommendation: File Form D within 15 days of first sale
   Deadline: 2024-03-30 (based on closing date 2024-03-15)
```

#### CA 25102(f) - Max 35 Investors
```python
{
    "name": "CA 25102(f) - Max 35 Investors",
    "category": "ca_securities",
    "rule_type": "count_limit",
    "threshold": 35,
    "description": "Section 25102(f) exemption limited to 35 purchasers",
    "citation": "CA Corp Code § 25102(f)"
}
```

**Evaluation (AI-assisted):**
```
❌ FAILED
   Investor count: 42 (extracted from subscription agreements)
   Limit: 35
   Overage: 7 investors
   Recommendation: Consider alternative exemption (e.g., Reg D 506(b))
```

**Compliance Score Calculation:**

```
Total Rules Evaluated: 20
├─ Passed: 15 (75%)
├─ Failed: 3 (15%)
└─ Warning: 2 (10%)

Overall Compliance Score: 75%

Breakdown by Category:
├─ CA Corp Code:    100% (12/12 passed)
├─ SEC Reg D:       75% (6/8 passed)
├─ CA Securities:   50% (3/6 passed)
└─ Governance:      90% (9/10 passed)
```

**Output:**
- Creates `ComplianceResult` records
- Calculates overall compliance score
- Generates recommendations
- Marks matter as "completed" or "flagged"

---

## 2.3 Compliance Engine

### Supported Jurisdictions

| Jurisdiction | Corporate Law | Securities Law | Coverage |
|--------------|---------------|----------------|----------|
| **California** | CA Corp Code | CA Securities Act | Comprehensive |
| **Delaware** | DGCL | DE Securities Act | Comprehensive |
| **New York** | NY BCL | Martin Act | Basic |
| **Texas** | TX BOC | TX Securities Act | Basic |
| **Federal** | N/A | SEC Regulations | Comprehensive |

### Rule Categories

#### 1. CA Corp Code (12 rules)
- Agent for service of process
- Board authorization requirements
- Shareholder meeting notices
- Merger vote thresholds
- Appraisal rights
- Certificate of incorporation requirements
- Bylaws requirements
- Stock certificate requirements
- Transfer restrictions
- Preemptive rights
- Cumulative voting
- Inspection rights

#### 2. SEC Reg D (8 rules)
- Form D filing (Rule 503)
- Accredited investor verification (Rule 506(c))
- No general solicitation (Rule 502(c))
- Max 35 non-accredited investors (Rule 506(b))
- Integration safe harbor (Rule 502(a))
- Disclosure requirements (Rule 502(b))
- Resale restrictions (Rule 502(d))
- Bad actor disqualification (Rule 506(d))

#### 3. CA Securities (6 rules)
- Section 25102(f) max 35 purchasers
- Notice filing with CA DFPI
- Accredited investor requirements
- No advertising/solicitation
- Issuer transaction requirement
- California purchaser limits

#### 4. DE Corp Law (10 rules)
- Certificate of Incorporation filing
- Foreign qualification in CA
- Board authorization
- Stockholder approval thresholds
- Appraisal rights notice
- Merger agreement requirements
- Certificate of merger
- Good standing certificate
- Registered agent designation
- Annual franchise tax

#### 5. HSR Act (4 rules)
- Filing threshold ($111.4M in 2024)
- Pre-merger notification
- Waiting period (30 days)
- Documentary requirements

#### 6. Governance (10 rules)
- Board size minimums
- Independent director requirements
- Committee composition
- Vote thresholds
- Quorum requirements
- Notice periods
- Protective provisions
- Information rights
- Registration rights
- Anti-dilution provisions

### Compliance Scoring Methodology

```
For each matter:

1. Filter applicable rules
   - By matter type (vc, m_and_a, formation, etc.)
   - By jurisdiction (CA, DE, etc.)
   - By deal value (for HSR)

2. Evaluate each rule
   - Deterministic: Check documents/data
   - AI-assisted: Use LLM for complex evaluation
   - Result: PASS, FAIL, WARNING, or N/A

3. Calculate scores
   - Category score = (passed / total) * 100
   - Overall score = weighted average of categories
   - Weighting: Critical categories (securities) weighted 2x

4. Assign status
   - 90-100%: Compliant (green)
   - 70-89%: Needs attention (yellow)
   - <70%: Non-compliant (red)
```

**Example Compliance Report:**

```
COMPLIANCE REPORT: Acme Corp Series A

Overall Score: 82% (Needs Attention)

Category Breakdown:
┌──────────────────┬────────┬────────┬────────┬────────┐
│ Category         │ Passed │ Failed │ Warn   │ Score  │
├──────────────────┼────────┼────────┼────────┼────────┤
│ CA Corp Code     │ 12     │ 0      │ 0      │ 100%   │
│ SEC Reg D        │ 6      │ 1      │ 1      │ 75%    │
│ CA Securities    │ 3      │ 2      │ 1      │ 50%    │
│ Governance       │ 9      │ 0      │ 1      │ 90%    │
└──────────────────┴────────┴────────┴────────┴────────┘

Critical Issues (2):
❌ SEC Reg D - Form D not filed
❌ CA 25102(f) - Exceeds 35 investor limit

Warnings (3):
⚠️  Missing accredited investor questionnaires
⚠️  Board size below recommended minimum
⚠️  No anti-dilution protection for common

Recommendations:
1. File Form D within 15 days of first sale
2. Consider Reg D 506(b) instead of 25102(f)
3. Collect accredited investor questionnaires
4. Expand board to 5 members
5. Add weighted average anti-dilution
```

---

## 2.4 Real-Time Notifications

### Telegram Integration

LexPilot sends real-time alerts to Telegram when key events occur.

#### Setup

1. Go to **📱 Telegram** tab in sidebar
2. Follow 4-step wizard:
   - Create bot with @BotFather
   - Get chat ID from @userinfobot
   - Enter credentials
   - Test connection

#### Notification Types

**Pipeline Started:**
```
🚀 Law-Lite Pipeline Started

Matter: Acme Corp Series A
Type: VC

Agents Lex → Petra → Gavel → Reese → Portia are processing...
```

**Pipeline Completed:**
```
Law-Lite Pipeline Complete

Matter: Acme Corp Series A
Status: ✅ COMPLETED

✓ 5 documents processed
✓ 12 fields extracted
⚠️ 3 issues detected
✓ Compliance: 82% (18/22 rules passed)
```

**Critical Issue Detected:**
```
🚨 Issue Detected [CRITICAL]

Matter: Acme Corp Series A
Type: Amount Inconsistency
Severity: CRITICAL

Review required in the Law-Lite dashboard.
```

**Matter Flagged:**
```
⚠️ Matter Flagged

Matter: Acme Corp Series A
Reason: Compliance score below 70%

3 critical issues require attention.
```

#### Configuration

```yaml
telegram_enabled: "true"
telegram_bot_token: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
telegram_chat_id: "890034905"
```

### Slack Integration (Roadmap)

Coming in Q2 2026:
- Slack app installation
- Channel-based notifications
- Interactive issue resolution
- Thread-based discussions

### Email Notifications (Roadmap)

Coming in Q2 2026:
- SMTP configuration
- Recipient lists by severity
- Daily digest option
- Custom email templates

---

## 2.5 Reporting & Analytics

### PDF Report Generation

Generate comprehensive deal summaries in PDF format.

#### Report Sections

1. **Executive Summary**
   - Matter overview
   - Key metrics
   - Overall compliance score
   - Critical issues summary

2. **Document Inventory**
   - List of all documents
   - Document types
   - Execution dates
   - Status

3. **Extracted Fields**
   - All structured data
   - Organized by document
   - Confidence scores

4. **Issues & Findings**
   - Critical issues
   - Warnings
   - Recommendations
   - Severity breakdown

5. **Compliance Report**
   - Rule-by-rule results
   - Category scores
   - Failed rules with citations
   - Remediation steps

6. **Agent Logs**
   - Processing timeline
   - Agent-by-agent results
   - Performance metrics

#### Example Report

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              LEXPILOT DEAL REPORT                   │
│                                                     │
│  Matter: Acme Corp Series A Financing               │
│  Client: Acme Corporation                           │
│  Date: April 18, 2026                               │
│                                                     │
└─────────────────────────────────────────────────────┘

EXECUTIVE SUMMARY

Matter Type: Venture Capital Financing
Deal Value: $5,000,000
Jurisdiction: California
Status: Needs Attention (82% compliance)

Key Metrics:
• Documents Processed: 5
• Fields Extracted: 24
• Issues Identified: 6 (2 critical, 3 warning, 1 info)
• Compliance Score: 82%
• Processing Time: 67 seconds

Critical Issues Requiring Attention:
1. SEC Form D not filed (deadline: March 30, 2024)
2. Exceeds CA 25102(f) 35-investor limit (42 investors)

---

DOCUMENT INVENTORY

1. TermSheet_AcmeCorp.pdf
   Type: Term Sheet
   Date: March 1, 2024
   Status: ✓ Processed

2. StockPurchaseAgreement.pdf
   Type: Stock Purchase Agreement
   Date: March 15, 2024
   Status: ✓ Processed

3. BoardResolution_20240315.pdf
   Type: Board Resolution
   Date: March 15, 2024
   Status: ✓ Processed

4. SubscriptionAgreement_Sequoia.pdf
   Type: Subscription Agreement
   Date: March 15, 2024
   Status: ✓ Processed

5. SubscriptionAgreement_A16Z.pdf
   Type: Subscription Agreement
   Date: March 15, 2024
   Status: ✓ Processed

---

EXTRACTED FIELDS

Term Sheet:
• Company Name: Acme Corporation
• Investors: Sequoia Capital, Andreessen Horowitz
• Investment Amount: $5,000,000
• Pre-Money Valuation: $20,000,000
• Post-Money Valuation: $25,000,000
• Price Per Share: $2.50
• Closing Date: March 15, 2024
• Board Composition: 2 founders, 2 investors, 1 independent

Stock Purchase Agreement:
• Purchaser: Sequoia Capital, Andreessen Horowitz
• Seller: Acme Corporation
• Purchase Price: $5,000,000
• Shares Purchased: 2,000,000
• Price Per Share: $2.50
• Closing Date: March 15, 2024

[... more fields ...]

---

ISSUES & FINDINGS

CRITICAL (2):
❌ SEC Form D Not Filed
   Category: SEC Reg D
   Description: Form D must be filed within 15 days of first sale
   Deadline: March 30, 2024
   Recommendation: File Form D immediately

❌ Exceeds 25102(f) Investor Limit
   Category: CA Securities
   Description: Section 25102(f) limited to 35 purchasers
   Found: 42 investors
   Overage: 7 investors
   Recommendation: Use Reg D 506(b) instead

WARNINGS (3):
⚠️  Missing Accredited Investor Questionnaires
⚠️  Board Size Below Recommended Minimum (3 vs 5)
⚠️  No Anti-Dilution Protection for Common Stock

INFO (1):
ℹ️  Consider Adding Drag-Along Rights

---

COMPLIANCE REPORT

Overall Score: 82% (18/22 rules passed)

CA Corp Code: 100% (12/12)
✓ Agent for service designated
✓ Board authorization obtained
✓ Certificate of incorporation compliant
[... all passed ...]

SEC Reg D: 75% (6/8)
✓ Accredited investor verification (506(c))
✓ No general solicitation
✓ Integration safe harbor
✓ Disclosure requirements met
✓ Resale restrictions included
✓ No bad actors
❌ Form D not filed
⚠️  35 investor limit exceeded (using 506(b))

CA Securities: 50% (3/6)
✓ Issuer transaction
✓ No advertising
✓ Accredited investors only
❌ 25102(f) 35 purchaser limit exceeded
❌ Notice filing not completed
⚠️  Missing investor questionnaires

Governance: 90% (9/10)
✓ Board authorization
✓ Stockholder approval
✓ Protective provisions
✓ Information rights
✓ Registration rights
✓ Preemptive rights waived
✓ Right of first refusal
✓ Co-sale rights
✓ Drag-along rights
⚠️  Board size below recommended

---

PROCESSING TIMELINE

March 15, 2024 14:32:15 - Documents uploaded (5 files)
March 15, 2024 14:32:16 - Lex: Classification started
March 15, 2024 14:32:17 - Lex: Completed (5 documents classified)
March 15, 2024 14:32:17 - Petra: OCR started
March 15, 2024 14:32:35 - Petra: OCR completed (5 documents)
March 15, 2024 14:32:35 - Petra: Field extraction started
March 15, 2024 14:32:50 - Petra: Completed (24 fields extracted)
March 15, 2024 14:32:50 - Gavel: Validation started
March 15, 2024 14:32:52 - Gavel: Completed (6 issues found)
March 15, 2024 14:32:52 - Reese: Analysis started
March 15, 2024 14:33:17 - Reese: Completed (contract analysis done)
March 15, 2024 14:33:17 - Portia: Compliance check started
March 15, 2024 14:33:37 - Portia: Completed (22 rules evaluated)
March 15, 2024 14:33:37 - Pipeline completed

Total Processing Time: 82 seconds

---

Generated by LexPilot v1.1.8
April 18, 2026 14:35:00 UTC
```

### Usage Analytics Dashboard

Track system usage and performance over time.

#### Metrics Tracked

**Volume Metrics:**
- Matters processed (total, by month)
- Documents analyzed (total, by type)
- Fields extracted (total, by document type)
- Issues detected (total, by severity)
- Compliance checks run (total, by category)

**Performance Metrics:**
- Average processing time (by agent)
- Success rate (by agent)
- Field extraction accuracy
- Classification accuracy
- Compliance score distribution

**Cost Metrics:**
- AI API calls (by provider)
- Token usage (input/output)
- Estimated cost (by provider)
- Cost per matter
- Cost savings vs manual review

#### Example Dashboard

```
USAGE ANALYTICS (Last 30 Days)

Volume:
┌─────────────────┬──────────┐
│ Metric          │ Count    │
├─────────────────┼──────────┤
│ Matters         │ 127      │
│ Documents       │ 453      │
│ Fields Extracted│ 1,824    │
│ Issues Detected │ 89       │
│ Compliance Runs │ 1,524    │
└─────────────────┴──────────┘

Performance:
┌─────────────────┬──────────┬──────────┐
│ Agent           │ Avg Time │ Success  │
├─────────────────┼──────────┼──────────┤
│ Lex             │ 0.5s     │ 100%     │
│ Petra           │ 20.3s    │ 95%      │
│ Gavel           │ 2.1s     │ 100%     │
│ Reese           │ 24.8s    │ 92%      │
│ Portia          │ 19.7s    │ 93%      │
└─────────────────┴──────────┴──────────┘

Cost Analysis:
┌─────────────────┬──────────┬──────────┐
│ Provider        │ Calls    │ Cost     │
├─────────────────┼──────────┼──────────┤
│ OpenRouter      │ 3,456    │ $0.00    │
│ Ollama          │ 0        │ $0.00    │
│ Claude          │ 0        │ $0.00    │
├─────────────────┼──────────┼──────────┤
│ Total           │ 3,456    │ $0.00    │
└─────────────────┴──────────┴──────────┘

ROI:
• Time Saved: 1,016 hours (127 matters × 8 hours)
• Cost Saved: $203,200 (1,016 hours × $200/hour)
• Processing Cost: $0 (free tier)
• Net Savings: $203,200
• ROI: ∞ (zero cost)
```

---

**Next Section:** [User Guide →](user-guide.md)
**Previous Section:** [← Overview](overview.md)

---

**Last Updated:** April 2026 | **Version:** 1.1.8
