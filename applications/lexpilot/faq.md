# FAQ & Troubleshooting

> **Quick Summary:** Frequently asked questions covering general usage, setup, configuration, troubleshooting, security, and compliance.

---

## General Questions

### What is LexPilot?

LexPilot is an AI-powered legal document processing platform that automates contract review, compliance checking, and risk analysis for corporate transactions. It processes documents through a five-agent pipeline (Lex → Petra → Gavel → Reese → Portia) to extract data, validate consistency, analyze contracts, and check regulatory compliance.

---

### What file formats are supported?

**Currently:** PDF only

**Requirements:**
- File extension: `.pdf`
- Max file size: 50 MB per file
- Max total: 500 MB per matter
- Searchable PDFs preferred (scanned PDFs work but may have lower accuracy)

**Roadmap:** Word (.docx), Excel (.xlsx), images (.jpg, .png)

---

### How long does processing take?

**Typical Processing Times:**
- Single document: 20-30 seconds
- 5-document deal: 60-90 seconds
- 10-document deal: 90-120 seconds

**Breakdown by Agent:**
- Lex (Classification): 0.5 seconds
- Petra (OCR + Extraction): 20 seconds
- Gavel (Validation): 2 seconds
- Reese (Analysis): 25 seconds
- Portia (Compliance): 20 seconds

**Factors Affecting Speed:**
- Document size and complexity
- AI provider (OpenRouter faster than Ollama)
- Network latency (for cloud AI)
- Server resources

---

### Can I process multiple matters simultaneously?

**Yes!** LexPilot uses async processing and can handle multiple matters concurrently.

**Limits:**
- No hard limit on concurrent matters
- Limited by server resources (CPU, RAM)
- AI provider rate limits (if using cloud AI)

**Recommendations:**
- Self-hosted: 5-10 concurrent matters
- Cloud deployment: 20+ concurrent matters with auto-scaling

---

### Is there a file size limit?

**Yes:**
- Per file: 50 MB maximum
- Per matter: 500 MB total recommended

**Why the limits:**
- Memory constraints during processing
- AI provider token limits
- Reasonable processing times

**Workarounds for large files:**
- Split large PDFs into smaller files
- Compress PDFs (reduce image quality)
- Use OCR preprocessing to reduce file size

---

### Can I delete a matter?

**Yes,** but be careful!

**What gets deleted:**
- The matter record
- All associated documents
- All extracted data
- All issues
- All compliance results

**Cannot be undone!**

**How to delete:**
1. Go to matter detail page
2. Click **Delete** button
3. Confirm deletion

**Alternative:** Archive matters instead of deleting (roadmap feature)

---

### How accurate is the AI?

**Overall Accuracy:**
- Document classification: 96%
- OCR text extraction: 95%+
- Field extraction: 91% average
- Compliance checking: 95%+

**Accuracy by Provider:**
- OpenRouter (gemini-pro-vision): 95%+
- Ollama (qwen2-vl): 88-92%
- Tesseract (fallback): 85%+

**Factors Affecting Accuracy:**
- Document quality (scanned vs digital)
- Handwriting (not supported)
- Complex layouts
- Non-standard terminology

**Confidence Scores:**
- 90-100%: High confidence (auto-accept)
- 70-89%: Medium confidence (review recommended)
- <70%: Low confidence (manual verification required)

---

### What happens if AI fails?

**Fallback Strategy:**

1. **Primary AI fails** → Try fallback provider
2. **All AI fails** → Mark document as "error" status
3. **User notified** → Can retry manually

**Error Handling:**
- Errors logged for debugging
- Matter status updated to "error"
- User can view error details
- Can re-run pipeline after fixing issue

**Common Causes:**
- AI provider timeout
- Invalid API key
- Rate limiting
- Network issues

**Solutions:**
- Check AI provider settings
- Verify API key is valid
- Wait and retry (for rate limits)
- Check network connectivity

---

### Can I use my own AI models?

**Yes!** LexPilot supports:

**Local AI (Ollama):**
- Run any Ollama-compatible model
- Full privacy (no data leaves your network)
- Examples: qwen2.5:14b, llama3.1:70b, mistral:7b

**Cloud AI:**
- OpenRouter (100+ models)
- Claude (Anthropic)
- Azure OpenAI (your own deployment)

**Custom Models:**
- Fine-tune your own models
- Deploy via Ollama
- Configure in Settings

**Roadmap:**
- Hugging Face integration
- Custom model upload
- Model fine-tuning UI

---

## Setup & Configuration

### Which AI provider should I use?

**Recommendations:**

**For Privacy (Recommended):**
- **Ollama** (local AI)
- Pros: 100% private, no cost, full control
- Cons: Slower, requires GPU for best performance
- Best for: Law firms, enterprises, regulated industries

**For Speed & Cost:**
- **OpenRouter** (cloud AI)
- Pros: Fast, free tier available, 100+ models
- Cons: Data sent to cloud (anonymized in hybrid mode)
- Best for: Startups, small teams, cost-conscious users

**For Quality:**
- **Claude** (Anthropic)
- Pros: Highest accuracy, best for complex documents
- Cons: Most expensive (~$0.05/document)
- Best for: High-value deals, critical documents

**Hybrid Approach:**
- Use Ollama for routine documents
- Use Claude for complex/critical documents
- Best of both worlds

---

### How do I configure Ollama?

**Step 1: Install Ollama**

```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

**Step 2: Pull Models**

```bash
# Vision model (for OCR)
ollama pull qwen2-vl

# Text model (for field extraction)
ollama pull qwen2.5:14b
```

**Step 3: Configure in LexPilot**

1. Go to **Settings**
2. Set **AI Provider** to `ollama`
3. Set **Ollama URL** to `http://localhost:11434`
4. Set **Ollama Model** to `qwen2.5:14b`
5. Set **Petra Vision Provider** to `ollama`
6. Set **Ollama Vision Model** to `qwen2-vl`
7. Click **Save Settings**

**Step 4: Test**

1. Create a test matter
2. Upload a document
3. Watch Agents tab
4. Verify processing completes

---

### Why is OpenRouter failing?

**Common Issues:**

**1. Invalid API Key**
- Error: `401 Unauthorized`
- Solution: Verify API key in Settings
- Get new key at https://openrouter.ai

**2. Rate Limiting**
- Error: `429 Too Many Requests`
- Solution: Wait 60 seconds and retry
- Or upgrade to paid tier

**3. Model Not Found**
- Error: `404 Model not found`
- Solution: Check model name spelling
- Use: `google/gemma-4-31b-it:free`

**4. Network Issues**
- Error: `Connection timeout`
- Solution: Check internet connection
- Verify firewall allows HTTPS to openrouter.ai

**5. Insufficient Credits**
- Error: `402 Payment Required`
- Solution: Add credits to OpenRouter account
- Or use free tier models

---

### How do I set up Telegram notifications?

**Complete Guide:**

See **📱 Telegram** tab in sidebar for step-by-step wizard.

**Quick Steps:**

1. Create bot with @BotFather
2. Get chat ID from @userinfobot
3. Go to Settings → Telegram
4. Enter bot token and chat ID
5. Click **Test Connection**
6. Click **Save**

**Troubleshooting:**

**Bot not responding:**
- Send `/start` to your bot first
- Verify bot token is correct
- Check bot is not blocked

**Wrong chat ID:**
- Use @userinfobot to get correct ID
- For groups: Use @getidsbot
- Group IDs are negative (e.g., `-1001234567890`)

**Test message not received:**
- Check chat ID is correct
- Verify bot has permission to send messages
- Check Telegram app is open

---

## Troubleshooting

### Pipeline stuck at "extracting"

**Symptoms:**
- Petra agent shows "Extracting fields..." for >5 minutes
- Progress bar stuck at same percentage
- No error message

**Causes:**
1. AI provider timeout
2. Large document (>20 pages)
3. Complex layout
4. Network issues

**Solutions:**

**1. Check AI Provider Status**
```bash
# For Ollama
curl http://localhost:11434/api/tags

# For OpenRouter
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**2. Check Logs**
```bash
# Docker
docker logs lexpilot | grep Petra

# Kubernetes
kubectl logs -f deployment/lexpilot -n lexpilot | grep Petra
```

**3. Restart Pipeline**
- Go to matter detail page
- Click **Retry Pipeline**
- Or delete document and re-upload

**4. Try Different AI Provider**
- Switch from Ollama to OpenRouter
- Or vice versa
- See which works better

---

### Low confidence scores (<70%)

**Symptoms:**
- Extracted fields show confidence <70%
- Fields marked for manual review
- Incorrect values extracted

**Causes:**
1. Poor document quality (scanned, low resolution)
2. Handwritten text
3. Complex layout
4. Non-standard terminology

**Solutions:**

**1. Re-upload Higher Quality Version**
- Scan at 300 DPI minimum
- Use color scanning
- Ensure good contrast

**2. Use Better AI Provider**
- Switch to OpenRouter (higher accuracy)
- Or use Claude for critical documents

**3. Manual Verification**
- Review and edit low-confidence fields
- Mark as verified
- System learns from corrections

**4. Pre-process Document**
- Convert to searchable PDF
- Clean up scans
- Remove watermarks/backgrounds

---

### Misclassified documents

**Symptoms:**
- Lex classified document as wrong type
- Expected "term_sheet" but got "unknown"
- Wrong compliance rules applied

**Causes:**
1. Non-standard filename
2. Ambiguous document type
3. Multiple document types in one file

**Solutions:**

**1. Use Descriptive Filenames**
```
Good: TermSheet_AcmeCorp_SeriesA.pdf
Bad: document.pdf, scan001.pdf
```

**2. Manual Override**
- Go to Documents tab
- Click document name
- Select correct type from dropdown
- Click **Update**
- Re-run pipeline

**3. Split Multi-Type Documents**
- If PDF contains multiple document types
- Split into separate files
- Upload individually

---

### Missing compliance rules

**Symptoms:**
- Expected rule not evaluated
- Compliance score seems incomplete
- Specific jurisdiction rules missing

**Causes:**
1. Wrong matter type selected
2. Wrong jurisdiction selected
3. Deal value below threshold (for HSR)
4. Rule not applicable to this transaction

**Solutions:**

**1. Verify Matter Settings**
- Go to matter detail page
- Click **Edit**
- Check matter type is correct
- Check jurisdiction is correct
- Update if needed

**2. Check Rule Applicability**
- Some rules only apply to specific matter types
- Example: HSR rules only for deals >$111.4M
- Example: CA 25102(f) only for CA securities

**3. Review Compliance Report**
- Click **Compliance** tab
- Check which rules were evaluated
- See "N/A" for non-applicable rules

**4. Contact Support**
- If rule should apply but doesn't
- Provide matter details
- We'll investigate

---

### Agent timeout errors

**Symptoms:**
- Agent shows "error" status
- Error message: "Timeout after 60 seconds"
- Pipeline stops

**Causes:**
1. AI provider slow response
2. Large document
3. Network latency
4. Server overloaded

**Solutions:**

**1. Increase Timeout**
```python
# In app/services/ai.py
async with httpx.AsyncClient(timeout=120.0) as client:  # Increase from 60 to 120
```

**2. Use Faster AI Provider**
- OpenRouter is faster than Ollama
- Claude is fastest but most expensive

**3. Split Large Documents**
- If document >50 pages
- Split into smaller files
- Process separately

**4. Retry**
- Click **Retry Pipeline**
- Often succeeds on second attempt

---

## Security & Compliance

### Is my data secure?

**Yes!** LexPilot offers multiple security options:

**Private Deployment:**
- 100% on-premises
- No data leaves your network
- Air-gapped operation supported
- Full control over all data

**Hybrid Deployment:**
- Documents stored locally
- Only anonymized text sent to cloud AI
- PII replaced with tokens
- Mapping stored locally

**Security Features:**
- Encryption at rest (optional)
- Encryption in transit (HTTPS)
- Audit logging
- No data retention by AI providers

---

### Is LexPilot GDPR compliant?

**Yes,** when deployed privately:

**GDPR Requirements:**
- ✅ Data minimization (only necessary data collected)
- ✅ Right to deletion (delete matters/documents)
- ✅ Data portability (export via API)
- ✅ Security measures (encryption, access controls)
- ✅ Data processing agreements (not needed for private deployment)

**Hybrid Deployment:**
- Anonymization ensures GDPR compliance
- No personal data sent to cloud
- Tokens cannot be reverse-engineered

**Cloud Deployment:**
- Requires data processing agreement with AI providers
- Check provider GDPR compliance
- Consider data residency requirements

---

### Is LexPilot HIPAA compliant?

**Yes,** for private deployment:

**HIPAA Requirements:**
- ✅ Administrative safeguards (access controls, audit logs)
- ✅ Physical safeguards (on-premises deployment)
- ✅ Technical safeguards (encryption, secure transmission)
- ✅ Business associate agreements (not needed for private)

**Not Recommended:**
- Cloud deployment (without BAA)
- Hybrid deployment (unless anonymization verified)

**Best Practice:**
- Use private deployment
- Enable encryption at rest
- Implement access controls
- Regular security audits

---

### Can I use LexPilot for attorney-client privileged documents?

**Yes,** with private deployment:

**Privilege Protection:**
- Documents never leave your servers
- No third-party access
- Air-gapped operation available
- Complete control over data

**Hybrid Deployment:**
- Anonymization protects privilege
- No attorney-client communications sent to cloud
- Only document structure/fields extracted

**Best Practice:**
- Use private deployment for privileged documents
- Implement access controls
- Maintain audit trail
- Document security measures

---

## Performance & Optimization

### How can I speed up processing?

**1. Use Faster AI Provider**
- OpenRouter: 8-12 seconds/document
- Claude: 6-10 seconds/document
- Ollama (CPU): 30-60 seconds/document
- Ollama (GPU): 10-20 seconds/document

**2. Optimize Ollama**
```bash
# Use GPU acceleration
nvidia-smi  # Verify GPU available

# Use faster models
ollama pull qwen2.5:7b  # Smaller, faster

# Increase concurrent requests
OLLAMA_NUM_PARALLEL=4 ollama serve
```

**3. Pre-process Documents**
- Convert to searchable PDF
- Reduce file size
- Remove unnecessary pages

**4. Batch Processing**
- Upload all documents at once
- Parallel processing is faster
- Avoid uploading one-by-one

---

### Why is Ollama slow?

**Common Causes:**

**1. CPU Inference (No GPU)**
- Solution: Add NVIDIA GPU
- Or use cloud AI instead

**2. Large Model**
- qwen2.5:70b is slow
- Solution: Use qwen2.5:14b or qwen2.5:7b

**3. Low RAM**
- Models need 16-32 GB RAM
- Solution: Upgrade RAM or use smaller model

**4. Other Processes**
- Ollama competing for resources
- Solution: Close other applications

**Benchmarks:**

| Model | CPU (16 cores) | GPU (RTX 4090) |
|-------|----------------|----------------|
| qwen2.5:7b | 15s | 5s |
| qwen2.5:14b | 30s | 10s |
| qwen2.5:70b | 120s | 25s |

---

**Next Section:** [Resources →](resources.md)
**Previous Section:** [← Comparison](comparison.md)

---

**Last Updated:** April 2026 | **Version:** 1.1.8
