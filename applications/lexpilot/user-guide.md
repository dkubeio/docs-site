# User Guide

> **Quick Summary:** Complete guide to using LexPilot for legal document processing, from creating matters to generating reports.

---

## 4.1 Getting Started

### First Login

When you first access LexPilot at `http://localhost:5310`, you'll see the dashboard:

```
┌─────────────────────────────────────────────────────────┐
│  ⚖️  LEXPILOT                         [Settings] [Docs] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 Dashboard                                           │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │   Matters    │ │  Documents   │ │    Issues    │   │
│  │      0       │ │      0       │ │      0       │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                         │
│  Recent Activity                                        │
│  (No matters yet - create your first matter!)          │
│                                                         │
│  Quick Actions:                                         │
│  [+ New Matter]  [Upload Documents]  [View Reports]    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Dashboard Overview

**Top Navigation:**
- **LexPilot Logo** - Click to return to dashboard
- **Settings** - Configure AI providers, Telegram, etc.
- **Docs** - Access this documentation

**Sidebar Navigation:**
- **Dashboard** - Overview and quick stats
- **Matters** - All legal matters/deals
- **Upload** - Upload documents
- **Documents** - All documents across matters
- **Doc Lab** - Document analysis tools
- **Issues** - Flagged items requiring attention
- **Compliance** - Compliance check results
- **Agents** - Real-time pipeline monitoring
- **Activity** - Audit log of all actions
- **Reports** - Generate PDF reports
- **Settings** - System configuration
- **📱 Telegram** - Notification setup

**Metrics Cards:**
- **Matters** - Total number of matters
- **Documents** - Total documents processed
- **Issues** - Total issues detected

**Recent Activity:**
- Timeline of recent actions
- Matter status changes
- Document uploads
- Agent completions

### Navigation Tips

**Keyboard Shortcuts:**
- `Ctrl+K` - Quick search (roadmap)
- `Ctrl+N` - New matter (roadmap)
- `Ctrl+U` - Upload document (roadmap)

**Breadcrumbs:**
```
Dashboard > Matters > Acme Corp Series A > Documents
```
Click any breadcrumb to navigate back.

**Status Indicators:**
- 🟢 Green - Completed successfully
- 🟡 Yellow - Needs attention
- 🔴 Red - Critical issues
- ⚪ Gray - Pending/not started

---

## 4.2 Matter Management

### 4.2.1 Creating Matters

**Step 1: Navigate to Matters**

Click **Matters** in sidebar → Click **+ New Matter** button

**Step 2: Fill in Matter Details**

```
┌─────────────────────────────────────────────┐
│  Create New Matter                          │
├─────────────────────────────────────────────┤
│                                             │
│  Matter Name *                              │
│  [Acme Corp Series A Financing         ]   │
│                                             │
│  Client Name *                              │
│  [Acme Corporation                     ]   │
│                                             │
│  Matter Type *                              │
│  [vc ▼]                                     │
│   • vc (Venture Capital)                    │
│   • m_and_a (Mergers & Acquisitions)        │
│   • formation (Company Formation)           │
│   • securities (Securities Offering)        │
│   • pe (Private Equity)                     │
│   • debt_finance (Debt Financing)           │
│   • corporate (General Corporate)           │
│                                             │
│  Deal Value                                 │
│  [$5,000,000                           ]   │
│                                             │
│  Entity Jurisdiction *                      │
│  [CA ▼]                                     │
│   • CA (California)                         │
│   • DE (Delaware)                           │
│   • NY (New York)                           │
│   • TX (Texas)                              │
│   • Other                                   │
│                                             │
│  [Cancel]              [Create Matter]      │
│                                             │
└─────────────────────────────────────────────┘
```

**Field Descriptions:**

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| **Matter Name** | Yes | Descriptive name for the deal | "Acme Corp Series A Financing" |
| **Client Name** | Yes | Company or entity name | "Acme Corporation" |
| **Matter Type** | Yes | Type of transaction | "vc" for venture capital |
| **Deal Value** | No | Transaction amount in USD | 5000000 |
| **Entity Jurisdiction** | Yes | State of incorporation | "CA" for California |

**Step 3: Click Create Matter**

Matter is created with status: `intake` (ready for documents)

### 4.2.2 Matter Types Explained

#### Venture Capital (vc)
```
Typical Documents:
• Term sheet
• Stock purchase agreement
• Subscription agreements
• Board resolution
• Accredited investor questionnaires
• Section 25102(f) notice (CA)
• SEC Form D

Compliance Checks:
• CA Corp Code (12 rules)
• SEC Reg D (8 rules)
• CA Securities (6 rules)
• Governance (10 rules)

Average Processing Time: 90 seconds
```

#### M&A (m_and_a)
```
Typical Documents:
• Stock/asset purchase agreement
• Board resolutions (buyer & seller)
• Shareholder approvals
• Disclosure schedules
• Opinion letters
• HSR filing (if >$111.4M)

Compliance Checks:
• CA Corp Code
• DE Corp Law
• HSR Act (if applicable)
• Governance

Average Processing Time: 120 seconds
```

#### Formation (formation)
```
Typical Documents:
• Articles of incorporation
• Bylaws
• Initial board resolution
• Stock issuance resolution
• 83(b) elections

Compliance Checks:
• CA Corp Code
• Governance
• Tax compliance

Average Processing Time: 60 seconds
```

#### Securities (securities)
```
Typical Documents:
• Private placement memorandum
• Subscription agreements
• SEC Form D
• Blue sky filings
• Accredited investor verification

Compliance Checks:
• SEC Reg D
• State securities laws
• Governance

Average Processing Time: 90 seconds
```

### 4.2.3 Viewing Matters

**Matters List View:**

```
┌─────────────────────────────────────────────────────────────┐
│  Matters                                    [+ New Matter]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Filter: [All ▼]  [vc ▼]  [CA ▼]  [Search...          ]   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Acme Corp Series A                          [View]  │   │
│  │ Client: Acme Corporation                            │   │
│  │ Type: vc  |  Value: $5M  |  Jurisdiction: CA        │   │
│  │ Status: 🟢 Completed  |  Compliance: 85%            │   │
│  │ Documents: 5  |  Issues: 2 critical                 │   │
│  │ Created: 2024-03-15  |  Updated: 2024-03-15         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ TechCo Acquisition                          [View]  │   │
│  │ Client: TechCo Inc                                  │   │
│  │ Type: m_and_a  |  Value: $50M  |  Jurisdiction: DE  │   │
│  │ Status: 🟡 Needs Attention  |  Compliance: 72%      │   │
│  │ Documents: 8  |  Issues: 5 warning                  │   │
│  │ Created: 2024-03-10  |  Updated: 2024-03-14         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Filters:**
- **Status** - All, Intake, Processing, Completed, Flagged
- **Type** - All, vc, m_and_a, formation, etc.
- **Jurisdiction** - All, CA, DE, NY, TX
- **Search** - Search by matter name or client name

**Sorting:**
- Click column headers to sort
- Default: Most recent first

### 4.2.4 Matter Detail View

Click **View** on any matter to see details:

```
┌─────────────────────────────────────────────────────────────┐
│  Acme Corp Series A Financing                               │
│  Status: 🟢 Completed  |  Compliance: 85%                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Overview] [Documents] [Issues] [Compliance] [Reports]    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  OVERVIEW                                           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Client: Acme Corporation                           │   │
│  │  Type: Venture Capital Financing                    │   │
│  │  Deal Value: $5,000,000                             │   │
│  │  Jurisdiction: California                           │   │
│  │  Created: March 15, 2024 14:32                      │   │
│  │  Last Updated: March 15, 2024 14:35                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  PROCESSING SUMMARY                                 │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Documents Processed: 5                             │   │
│  │  Fields Extracted: 24                               │   │
│  │  Issues Detected: 2 critical, 3 warning             │   │
│  │  Compliance Score: 85% (18/22 rules passed)         │   │
│  │  Processing Time: 82 seconds                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  CRITICAL ISSUES                                    │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  🚨 SEC Form D Not Filed                           │   │
│  │     Deadline: March 30, 2024                        │   │
│  │     [View Details]                                  │   │
│  │                                                     │   │
│  │  🚨 Exceeds 25102(f) Investor Limit                │   │
│  │     Found: 42 investors | Limit: 35                 │   │
│  │     [View Details]                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Tabs:**
- **Overview** - Summary and key metrics
- **Documents** - All uploaded documents
- **Issues** - Flagged items requiring attention
- **Compliance** - Rule-by-rule compliance results
- **Reports** - Generate and download PDF reports

### 4.2.5 Editing Matters

Click **Edit** button on matter detail page:

```
Editable Fields:
• Matter name
• Client name
• Deal value
• Entity jurisdiction

Non-editable:
• Matter type (set at creation)
• Status (managed by pipeline)
• Created date
```

### 4.2.6 Deleting Matters

Click **Delete** button → Confirm deletion

**Warning:** This permanently deletes:
- The matter record
- All associated documents
- All extracted data
- All issues and compliance results

**Cannot be undone!**

---

## 4.3 Working with Documents

### 4.3.1 Uploading Documents

**Method 1: Upload Page**

1. Click **Upload** in sidebar
2. Select matter from dropdown
3. Drag & drop PDF files or click **Browse**
4. Click **Upload**

```
┌─────────────────────────────────────────────┐
│  Upload Documents                           │
├─────────────────────────────────────────────┤
│                                             │
│  Select Matter *                            │
│  [Acme Corp Series A ▼]                     │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │                                     │   │
│  │   Drag & drop PDF files here        │   │
│  │                                     │   │
│  │   or                                │   │
│  │                                     │   │
│  │   [Browse Files]                    │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Selected Files:                            │
│  • TermSheet_AcmeCorp.pdf (1.2 MB)         │
│  • StockPurchaseAgreement.pdf (3.5 MB)     │
│  • BoardResolution.pdf (0.8 MB)            │
│                                             │
│  [Cancel]                    [Upload]       │
│                                             │
└─────────────────────────────────────────────┘
```

**Method 2: From Matter Detail Page**

1. Go to matter detail page
2. Click **Documents** tab
3. Click **+ Upload Document**
4. Select files and upload

**Supported Formats:**
- PDF only
- Max file size: 50 MB per file
- Max total: 500 MB per matter

**File Naming Best Practices:**

✅ **Good:**
- `TermSheet_AcmeCorp_2024.pdf`
- `SPA_AcmeCorp_BuyerCo.pdf`
- `BoardResolution_20240315.pdf`
- `NDA_AcmeCorp_Mutual.pdf`

❌ **Avoid:**
- `document.pdf`
- `scan001.pdf`
- `untitled.pdf`
- `final_final_v3.pdf`

**Why naming matters:**
- Lex agent uses filename for classification
- Better organization and searchability
- Easier to identify missing documents

### 4.3.2 Document Processing

After upload, documents automatically enter the pipeline:

**Processing Stages:**

```
Upload Complete
     │
     ▼
┌─────────────────┐
│  INTAKE         │  Lex classifies document type
│  Status: intake │  • Pattern matching on filename
└────────┬────────┘  • ~0.5 seconds
         │
         ▼
┌─────────────────┐
│  EXTRACTING     │  Petra performs OCR and field extraction
│  Status: extract│  • Vision model extracts text
└────────┬────────┘  • Language model parses fields
         │           • ~20 seconds
         ▼
┌─────────────────┐
│  VALIDATING     │  Gavel runs deterministic checks
│  Status: validat│  • Entity name consistency
└────────┬────────┘  • Amount matching
         │           • Date conflicts
         ▼           • ~2 seconds
┌─────────────────┐
│  ANALYZING      │  Reese performs contract analysis
│  Status: analyzin│  • Risk identification
└────────┬────────┘  • Obligation extraction
         │           • ~25 seconds
         ▼
┌─────────────────┐
│  COMPLIANCE     │  Portia checks regulatory compliance
│  Status: complian│  • 50+ rules evaluated
└────────┬────────┘  • Jurisdiction-specific
         │           • ~20 seconds
         ▼
┌─────────────────┐
│  COMPLETED      │  Processing complete
│  Status: complete│  • Report generated
└─────────────────┘  • Notifications sent
```

**Monitor Progress:**

Go to **Agents** tab to watch real-time processing:

```
┌─────────────────────────────────────────────────────────┐
│  Agent Pipeline - Acme Corp Series A                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ✅ Lex       Classified 5 documents (0.5s)            │
│  ✅ Petra     Extracted 24 fields (20.3s)              │
│  ✅ Gavel     Found 6 issues (2.1s)                    │
│  🔄 Reese     Analyzing contracts... 60%               │
│  ⏳ Portia    Waiting...                               │
│                                                         │
│  Overall Progress: 75%                                  │
│  Elapsed Time: 48 seconds                               │
│  Estimated Remaining: 15 seconds                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Status Indicators:**
- ✅ Completed successfully
- 🔄 Currently processing
- ⏳ Waiting in queue
- ❌ Failed (check logs)

### 4.3.3 Viewing Documents

**Documents Tab (in Matter):**

```
┌─────────────────────────────────────────────────────────┐
│  Documents (5)                      [+ Upload Document] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 📄 TermSheet_AcmeCorp.pdf                 [View] │ │
│  │ Type: Term Sheet  |  Size: 1.2 MB                │ │
│  │ Date: March 1, 2024  |  Status: ✅ Processed    │ │
│  │ Fields: 8 extracted  |  Confidence: 92%          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 📄 StockPurchaseAgreement.pdf         [View]     │ │
│  │ Type: Stock Purchase Agreement  |  Size: 3.5 MB  │ │
│  │ Date: March 15, 2024  |  Status: ✅ Processed   │ │
│  │ Fields: 12 extracted  |  Confidence: 88%         │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  [... more documents ...]                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Document Detail View:**

Click **View** to see extracted data:

```
┌─────────────────────────────────────────────────────────┐
│  TermSheet_AcmeCorp.pdf                                 │
│  Type: Term Sheet  |  Size: 1.2 MB  |  Pages: 5        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Extracted Fields] [Raw Text] [Original PDF]          │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  EXTRACTED FIELDS                                 │ │
│  ├───────────────────────────────────────────────────┤ │
│  │  Company Name: Acme Corporation                   │ │
│  │  Confidence: 95%  [Edit]                          │ │
│  │                                                   │ │
│  │  Investor Names: Sequoia Capital, A16Z           │ │
│  │  Confidence: 92%  [Edit]                          │ │
│  │                                                   │ │
│  │  Investment Amount: $5,000,000                    │ │
│  │  Confidence: 98%  [Edit]                          │ │
│  │                                                   │ │
│  │  Pre-Money Valuation: $20,000,000                 │ │
│  │  Confidence: 95%  [Edit]                          │ │
│  │                                                   │ │
│  │  Post-Money Valuation: $25,000,000                │ │
│  │  Confidence: 95%  [Edit]                          │ │
│  │                                                   │ │
│  │  Price Per Share: $2.50                           │ │
│  │  Confidence: 98%  [Edit]                          │ │
│  │                                                   │ │
│  │  Closing Date: March 15, 2024                     │ │
│  │  Confidence: 90%  [Edit]                          │ │
│  │                                                   │ │
│  │  Board Composition: 2 founders, 2 investors, 1 ind│ │
│  │  Confidence: 85%  [Edit]                          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.3.4 Editing Extracted Fields

Click **[Edit]** next to any field:

```
┌─────────────────────────────────────┐
│  Edit Field: Investment Amount      │
├─────────────────────────────────────┤
│                                     │
│  Current Value:                     │
│  $5,000,000                         │
│                                     │
│  New Value:                         │
│  [$5,500,000                   ]   │
│                                     │
│  Confidence: 98% → Manual Edit      │
│                                     │
│  [Cancel]              [Save]       │
│                                     │
└─────────────────────────────────────┘
```

**When to edit:**
- AI extracted wrong value
- Confidence score is low (<70%)
- Value changed after upload
- Manual correction needed

**Note:** Edits are logged in activity history.

### 4.3.5 Deleting Documents

Click **Delete** button on document → Confirm

**Warning:** This deletes:
- The document file
- All extracted fields
- Related issues
- Cannot be undone

**Impact on Matter:**
- Matter may need re-processing
- Compliance score may change
- Issues may be resolved or new ones created

---

## 4.4 Issue Management

### 4.4.1 Viewing Issues

Click **Issues** in sidebar to see all flagged items:

```
┌─────────────────────────────────────────────────────────┐
│  Issues (15)                                            │
│  Filter: [All ▼] [Critical ▼] [All Matters ▼]          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 🚨 CRITICAL                                       │ │
│  │ Amount Inconsistency                              │ │
│  │ Matter: Acme Corp Series A                        │ │
│  │                                                   │ │
│  │ Purchase price mismatch:                          │ │
│  │ • Term Sheet: $5,000,000                          │ │
│  │ • Stock Purchase Agreement: $5,500,000            │ │
│  │ • Difference: $500,000                            │ │
│  │                                                   │ │
│  │ Recommendation: Verify correct amount and update  │ │
│  │ documents accordingly.                            │ │
│  │                                                   │ │
│  │ [View Matter] [Mark Resolved] [Add Note]          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 🚨 CRITICAL                                       │ │
│  │ SEC Form D Not Filed                              │ │
│  │ Matter: Acme Corp Series A                        │ │
│  │                                                   │ │
│  │ Form D must be filed within 15 days of first sale.│ │
│  │ Closing Date: March 15, 2024                      │ │
│  │ Deadline: March 30, 2024                          │ │
│  │ Days Remaining: 15                                │ │
│  │                                                   │ │
│  │ Recommendation: File Form D immediately at        │ │
│  │ www.sec.gov/edgar                                 │ │
│  │                                                   │ │
│  │ [View Matter] [Mark Resolved] [Add Note]          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ ⚠️  WARNING                                       │ │
│  │ Missing Accredited Investor Questionnaires        │ │
│  │ Matter: Acme Corp Series A                        │ │
│  │                                                   │ │
│  │ No accredited investor questionnaires found.      │ │
│  │ Required for Reg D 506(c) offerings.              │ │
│  │                                                   │ │
│  │ Recommendation: Collect and upload questionnaires │ │
│  │ from all investors.                               │ │
│  │                                                   │ │
│  │ [View Matter] [Mark Resolved] [Add Note]          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.4.2 Issue Severity Levels

| Severity | Icon | Meaning | Action Required |
|----------|------|---------|-----------------|
| **Critical** | 🚨 | Must be resolved before closing | Immediate |
| **Warning** | ⚠️ | Should be addressed | Soon |
| **Info** | ℹ️ | Informational only | Optional |

**Critical Issues Examples:**
- Amount mismatches
- Entity name inconsistencies
- Missing required documents
- Failed compliance rules
- Date conflicts

**Warning Issues Examples:**
- Missing optional documents
- Low confidence extractions
- Governance recommendations
- Best practice suggestions

**Info Issues Examples:**
- Document classification notes
- Processing statistics
- Optimization suggestions

### 4.4.3 Resolving Issues

**Option 1: Mark as Resolved**

Click **[Mark Resolved]** → Add resolution note → Save

```
┌─────────────────────────────────────┐
│  Mark Issue as Resolved             │
├─────────────────────────────────────┤
│                                     │
│  Issue: Amount Inconsistency        │
│                                     │
│  Resolution Note:                   │
│  ┌─────────────────────────────┐   │
│  │ Verified with client that   │   │
│  │ correct amount is $5.5M.    │   │
│  │ Updated term sheet to match.│   │
│  └─────────────────────────────┘   │
│                                     │
│  Resolved By: John Doe              │
│  Date: March 16, 2024               │
│                                     │
│  [Cancel]        [Mark Resolved]    │
│                                     │
└─────────────────────────────────────┘
```

**Option 2: Fix Underlying Problem**

1. Navigate to matter/document
2. Edit extracted fields or upload corrected document
3. Re-run pipeline
4. Issue automatically resolved if fix is correct

**Option 3: Add Note**

Click **[Add Note]** to document investigation or action plan:

```
Notes on this issue:
• 2024-03-16 10:30 - Contacted client for clarification
• 2024-03-16 14:15 - Client confirmed $5.5M is correct
• 2024-03-16 15:00 - Updated term sheet, re-uploaded
```

### 4.4.4 Issue Filters

**Filter by Severity:**
- All
- Critical only
- Warning only
- Info only

**Filter by Matter:**
- All matters
- Specific matter

**Filter by Status:**
- Open (unresolved)
- Resolved
- All

**Sort by:**
- Severity (critical first)
- Date (newest first)
- Matter name

---

## 4.5 Compliance Checking

### 4.5.1 Viewing Compliance Results

Click **Compliance** in sidebar or **Compliance** tab in matter:

```
┌─────────────────────────────────────────────────────────┐
│  Compliance Report - Acme Corp Series A                 │
│  Overall Score: 82% (18/22 rules passed)                │
│  Status: 🟡 Needs Attention                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [By Category] [By Rule] [Failed Only]                 │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  CA CORP CODE                          100% (12/12)│ │
│  ├───────────────────────────────────────────────────┤ │
│  │  ✅ Agent for service designated                  │ │
│  │  ✅ Board authorization obtained                  │ │
│  │  ✅ Certificate of incorporation compliant        │ │
│  │  ✅ Bylaws requirements met                       │ │
│  │  ✅ Stock certificates issued                     │ │
│  │  ✅ Transfer restrictions documented              │ │
│  │  ✅ Preemptive rights addressed                   │ │
│  │  ✅ Cumulative voting disclosed                   │ │
│  │  ✅ Inspection rights granted                     │ │
│  │  ✅ Shareholder meeting notice proper             │ │
│  │  ✅ Merger vote threshold met                     │ │
│  │  ✅ Appraisal rights notice given                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  SEC REG D                              75% (6/8) │ │
│  ├───────────────────────────────────────────────────┤ │
│  │  ✅ Accredited investor verification (506(c))     │ │
│  │  ✅ No general solicitation                       │ │
│  │  ✅ Integration safe harbor                       │ │
│  │  ✅ Disclosure requirements met                   │ │
│  │  ✅ Resale restrictions included                  │ │
│  │  ✅ No bad actors                                 │ │
│  │  ❌ Form D not filed                              │ │
│  │  ⚠️  35 investor limit exceeded (using 506(b))   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  CA SECURITIES                          50% (3/6) │ │
│  ├───────────────────────────────────────────────────┤ │
│  │  ✅ Issuer transaction                            │ │
│  │  ✅ No advertising                                │ │
│  │  ✅ Accredited investors only                     │ │
│  │  ❌ 25102(f) 35 purchaser limit exceeded          │ │
│  │  ❌ Notice filing not completed                   │ │
│  │  ⚠️  Missing investor questionnaires             │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  GOVERNANCE                             90% (9/10)│ │
│  ├───────────────────────────────────────────────────┤ │
│  │  ✅ Board authorization                           │ │
│  │  ✅ Stockholder approval                          │ │
│  │  ✅ Protective provisions                         │ │
│  │  ✅ Information rights                            │ │
│  │  ✅ Registration rights                           │ │
│  │  ✅ Preemptive rights waived                      │ │
│  │  ✅ Right of first refusal                        │ │
│  │  ✅ Co-sale rights                                │ │
│  │  ✅ Drag-along rights                             │ │
│  │  ⚠️  Board size below recommended                │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.5.2 Understanding Compliance Scores

**Score Ranges:**

| Score | Status | Color | Meaning |
|-------|--------|-------|---------|
| 90-100% | ✅ Compliant | Green | Excellent, ready to close |
| 70-89% | 🟡 Needs Attention | Yellow | Address issues before closing |
| <70% | 🔴 Non-Compliant | Red | Critical issues, cannot close |

**Category Weights:**

Not all categories are equally important:

| Category | Weight | Rationale |
|----------|--------|-----------|
| SEC Reg D | 2x | Federal securities law |
| CA Securities | 2x | State securities law |
| CA Corp Code | 1x | Corporate governance |
| Governance | 1x | Best practices |

**Weighted Score Calculation:**

```
Example:
SEC Reg D: 75% × 2 = 150 points
CA Securities: 50% × 2 = 100 points
CA Corp Code: 100% × 1 = 100 points
Governance: 90% × 1 = 90 points

Total: 440 points / 6 weights = 73.3%
Rounded: 73% (Needs Attention)
```

### 4.5.3 Rule Details

Click any rule to see details:

```
┌─────────────────────────────────────────────────────────┐
│  Rule: SEC Reg D - Form D Filing                       │
│  Status: ❌ FAILED                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Category: SEC Reg D                                    │
│  Citation: 17 CFR § 230.503                             │
│                                                         │
│  Description:                                           │
│  Form D must be filed with the SEC within 15 days of   │
│  the first sale of securities in a Regulation D         │
│  offering.                                              │
│                                                         │
│  Evaluation:                                            │
│  ❌ Form D not found in uploaded documents              │
│                                                         │
│  Deadline:                                              │
│  March 30, 2024 (15 days after closing: March 15, 2024)│
│  Days Remaining: 15                                     │
│                                                         │
│  Recommendation:                                        │
│  File Form D immediately at www.sec.gov/edgar           │
│                                                         │
│  Required Information:                                  │
│  • Issuer name and address                              │
│  • Offering amount and type                             │
│  • Exemption claimed (Rule 506(b) or 506(c))            │
│  • Investor information                                 │
│  • Executive officer signatures                         │
│                                                         │
│  Resources:                                             │
│  • SEC Form D Instructions: [Link]                      │
│  • EDGAR Filing Guide: [Link]                           │
│                                                         │
│  [Mark as Resolved] [Add Note] [Close]                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.5.4 Jurisdiction-Specific Rules

**California (CA):**
- CA Corp Code (12 rules)
- CA Securities Act (6 rules)
- Total: 18 CA-specific rules

**Delaware (DE):**
- DE General Corporation Law (10 rules)
- DE Securities Act (4 rules)
- Total: 14 DE-specific rules

**Federal:**
- SEC Reg D (8 rules)
- HSR Act (4 rules if deal >$111.4M)
- Total: 8-12 federal rules

**All Jurisdictions:**
- Governance (10 rules)
- Total: 10 universal rules

**Example for CA VC Deal:**
```
Applicable Rules:
• CA Corp Code: 12 rules
• CA Securities: 6 rules
• SEC Reg D: 8 rules
• Governance: 10 rules
Total: 36 rules evaluated
```

---

## 4.6 Generating Reports

### 4.6.1 PDF Report Generation

**Step 1: Navigate to Reports**

Go to matter detail page → Click **Reports** tab

**Step 2: Generate Report**

Click **[Generate PDF Report]** button

```
┌─────────────────────────────────────┐
│  Generate Report                    │
├─────────────────────────────────────┤
│                                     │
│  Report Type:                       │
│  ● Comprehensive (recommended)      │
│  ○ Executive Summary                │
│  ○ Compliance Only                  │
│  ○ Issues Only                      │
│                                     │
│  Include:                           │
│  ☑ Executive summary                │
│  ☑ Document inventory               │
│  ☑ Extracted fields                 │
│  ☑ Issues & findings                │
│  ☑ Compliance report                │
│  ☑ Agent logs                       │
│  ☑ Recommendations                  │
│                                     │
│  Format:                            │
│  ● PDF                              │
│  ○ Word (roadmap)                   │
│  ○ Excel (roadmap)                  │
│                                     │
│  [Cancel]        [Generate Report]  │
│                                     │
└─────────────────────────────────────┘
```

**Step 3: Download Report**

Report generates in 5-10 seconds → Click **[Download]**

### 4.6.2 Report Types

**Comprehensive Report:**
- All sections included
- 15-30 pages typical
- Best for: Final deal review, client delivery

**Executive Summary:**
- High-level overview only
- 2-5 pages
- Best for: Quick review, management updates

**Compliance Only:**
- Compliance results and recommendations
- 5-10 pages
- Best for: Regulatory review, compliance team

**Issues Only:**
- Flagged items and resolutions
- 3-8 pages
- Best for: Issue tracking, remediation planning

### 4.6.3 Report Sections

**1. Executive Summary**
- Matter overview
- Key metrics (documents, fields, issues)
- Overall compliance score
- Critical issues requiring attention

**2. Document Inventory**
- List of all documents
- Document types and dates
- Processing status
- File sizes

**3. Extracted Fields**
- All structured data
- Organized by document
- Confidence scores
- Manual edits noted

**4. Issues & Findings**
- Critical issues
- Warnings
- Info items
- Recommendations
- Resolution status

**5. Compliance Report**
- Overall score
- Category breakdown
- Rule-by-rule results
- Failed rules with citations
- Remediation steps

**6. Agent Logs**
- Processing timeline
- Agent-by-agent results
- Performance metrics
- Error logs (if any)

**7. Recommendations**
- Next steps
- Best practices
- Risk mitigation
- Optimization suggestions

### 4.6.4 Customizing Reports

**Logo & Branding (Roadmap):**
- Upload firm logo
- Custom color scheme
- Firm name and address
- Contact information

**Template Customization (Roadmap):**
- Custom section order
- Add/remove sections
- Custom headers/footers
- Watermarks

---

## 4.7 Settings & Configuration

### 4.7.1 Accessing Settings

Click **Settings** in sidebar

### 4.7.2 AI Provider Settings

```
┌─────────────────────────────────────────────────────────┐
│  AI Provider Configuration                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Primary AI Provider:                                   │
│  [openrouter ▼]                                         │
│   • ollama (Local LLM)                                  │
│   • openrouter (Cloud API)                              │
│   • securellm (DKubeX Platform)                         │
│   • claude (Anthropic)                                  │
│                                                         │
│  OpenRouter Configuration:                              │
│  API Key: [sk-or-v1-••••••••••••••••]                  │
│  Base URL: [https://openrouter.ai/api/v1]              │
│  Model: [google/gemma-4-31b-it:free ▼]                  │
│                                                         │
│  Ollama Configuration (Fallback):                       │
│  URL: [http://localhost:11434]                          │
│  Model: [qwen2.5:14b]                                   │
│                                                         │
│  [Test Connection] [Save Settings]                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Test Connection:**
- Verifies API key is valid
- Checks model availability
- Tests latency
- Displays result

### 4.7.3 Petra OCR Settings

```
┌─────────────────────────────────────────────────────────┐
│  Petra OCR Configuration                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Vision Provider (OCR):                                 │
│  [openrouter ▼]                                         │
│                                                         │
│  OpenRouter Vision Model:                               │
│  [google/gemini-pro-vision ▼]                           │
│                                                         │
│  Text Provider (Field Extraction):                      │
│  [openrouter ▼]                                         │
│                                                         │
│  Fallback to Tesseract if vision fails:                 │
│  ☑ Enabled                                              │
│                                                         │
│  [Save Settings]                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.7.4 Telegram Notifications

See dedicated **📱 Telegram** tab for full setup wizard.

Quick settings:

```
Telegram Notifications:
☑ Enabled

Bot Token: [1234567890:ABC••••••••]
Chat ID: [890034905]

[Test Connection] [Save]
```

### 4.7.5 System Settings

```
Database:
• Type: SQLite
• Location: ./lexpilot.db
• Size: 15.2 MB
• [Backup Database]

File Storage:
• Location: ./uploads
• Size: 2.3 GB
• Documents: 453 files
• [Clean Up Old Files]

Logging:
• Level: INFO
• Retention: 30 days
• [View Logs] [Download Logs]
```

---

**Next Section:** [Use Cases →](use-cases.md)
**Previous Section:** [← Features](features.md)

---

**Last Updated:** April 2026 | **Version:** 1.1.8
