# Getting Started with Mortgage-Lite

This guide will help you set up and run Mortgage-Lite for the first time.

## Prerequisites

### Required
- **Python 3.12+**
- **Docker** (for containerized deployment)
- **Ollama** (for local LLM processing)

### Optional
- **Claude CLI** (for cloud-based compliance checking)
- **PostgreSQL** (for production deployments)
- **Telegram Bot** (for notifications)

## Installation

### Option 1: Local Development

#### 1. Clone the Repository
```bash
git clone https://github.com/dkubeio/mortgage-lite.git
cd mortgage-lite
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Set Up Environment Variables
Create a `.env` file in the project root:

```bash
# Database (SQLite for development)
DATABASE_URL=sqlite+aiosqlite:///./mortgage-lite.db

# Server Configuration
HOST=0.0.0.0
PORT=5300

# AI Configuration - Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:35b

# AI Configuration - Claude (Cloud)
CLAUDE_BIN=claude
CLAUDE_MODEL=sonnet
ANTHROPIC_API_KEY=your_key_here

# AI Configuration - SecureLLM (Local Inference)
# For Kubernetes (same namespace: dkubex-apps)
# Models are discovered automatically from the gateway
SECURELLM_BASE_URL=http://securellm/securellm/v1
SECURELLM_API_KEY=your_api_key_here

# API Keys (optional)
OPENAI_API_KEY=your_key_here

# Pipeline Configuration
DEFAULT_PIPELINE_TYPE=underwriting

# Features
ANONYMIZATION_ENABLED=true
ENABLE_OPTIMIZED_PIPELINE=false
ENABLE_PDF_VIEWER=true
ENABLE_SERVICING_PIPELINE=true
ENABLE_QC_PIPELINE=true

# DKubeX Integration (optional)
DKUBEX_BASE_PATH=
```

#### 4. Install Ollama and Pull Models
```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull required models
ollama pull qwen3.5:35b
```

#### 5. Initialize Database and Load Demo Data
```bash
# Generate demo data
python3 scripts/generate_demo_data.py

# Load demo applications
python3 scripts/load_demo.py
```

#### 6. Start the Application
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 5300 --reload
```

#### 7. Access the Application
Open your browser and navigate to:
```
http://localhost:5300
```

### Option 2: Docker Deployment

#### 1. Build the Docker Image
```bash
docker build -t mortgage-lite:latest .
```

#### 2. Run the Container
```bash
docker run -d \
  -p 5300:5300 \
  -v $(pwd)/uploads:/app/uploads \
  -e DATABASE_URL=sqlite+aiosqlite:///./mortgage-lite.db \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --name mortgage-lite \
  mortgage-lite:latest
```

#### 3. Access the Application
```
http://localhost:5300
```

### Option 3: Kubernetes Deployment

#### 1. Install with Helm
```bash
helm repo add dkubeio https://dkubeio.github.io/helm-charts
helm repo update

helm install mortgage-lite dkubeio/mortgage-lite \
  --set image.tag=latest \
  --set env.OLLAMA_BASE_URL=http://ollama-service:11434
```

#### 2. Access via Port Forward
```bash
kubectl port-forward svc/mortgage-lite 5300:5300
```

## First Steps

### 1. Explore the Dashboard
The main dashboard shows:
- Application statistics
- Agent status (8 agents across 3 pipelines)
- Recent activity
- System metrics
- Pipeline selector (Underwriting, Servicing, Quality Control)

### 2. Upload a Test Application
1. Click **"Upload"** in the navigation
2. Select pipeline type:
   - **Underwriting**: For loan origination
   - **Servicing**: For loan transfer validation
   - **Quality Control**: For post-close audit
3. Fill in applicant details:
   - Name: John Smith
   - Loan Type: Purchase
   - Loan Amount: $350,000
   - Property Value: $450,000
4. Upload documents (W-2, bank statements, etc.)
5. Click **"Submit Application"**

### 3. Run the Pipeline
1. Navigate to **"Applications"**
2. Find your application in the Kanban board
3. Click **"Run Pipeline"** on the application card
4. Watch as agents process the application through each stage

### 4. Review Results
After processing completes:
- Check **"Anomalies"** for any detected issues
- Use **"PDF Viewer"** to inspect documents with highlighted fields
- Review **"Compliance"** checks (underwriting pipeline)
- View the **"Report"** with executive summary
- Examine **"Metrics"** for performance data

### 5. Explore PDF Viewer
The anomaly inspector includes an inline PDF viewer:
1. Click on any anomaly in the list
2. Related documents appear in tabs
3. Navigate pages with Prev/Next buttons
4. Zoom in/out for detailed inspection
5. Flagged fields are highlighted with bounding boxes

## Demo Mode

Mortgage-Lite includes three pre-configured demo applications:

### Load Demo Data
```bash
python3 scripts/load_demo.py --reset
```

This creates three applications:
1. **John Smith** - Clean purchase loan (expected: APPROVED)
2. **Catherine Vellotti** - Refinance with 7 anomalies (expected: FLAGGED)
3. **Maria Garcia** - FHA loan with conditions (expected: CONDITIONALLY APPROVED)

### Run Demo Pipeline
```bash
# Start the server
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 5300

# In the UI, click "Run Pipeline" on each demo application
```

## Configuration

### AI Model Selection

#### Local Models (Privacy-Safe)

**Ollama**
```bash
# Ana agent uses local models for PII processing
OLLAMA_MODEL=qwen3.5:35b

# Alternative models
OLLAMA_MODEL=nemotron:70b
OLLAMA_MODEL=llama3.1:70b
```

**SecureLLM (Local Inference Server)**
```bash
# Use SecureLLM for local inference with OpenAI-compatible API
# Kubernetes service DNS (same namespace: dkubex-apps)
SECURELLM_BASE_URL=http://securellm/securellm/v1
SECURELLM_API_KEY=your_api_key

# SecureLLM provides chat completions endpoint
# Compatible with OpenAI API format
# Available models are discovered automatically from the gateway
# Ana and Rex agents will use SecureLLM if models are available,
# otherwise fall back to Ollama
```

#### Cloud Models (Anonymized Data Only)
```bash
# Claire agent uses Claude for compliance
CLAUDE_MODEL=sonnet
CLAUDE_MODEL=opus
CLAUDE_MODEL=haiku
```

### Anonymization

Enable/disable PII anonymization:
```bash
ANONYMIZATION_ENABLED=true
```

When enabled:
- Local agents (Iris, Rex, Val, Ana) process raw data
- Data is anonymized before Claire (cloud) processing
- Results are deanonymized before Max (delivery)

### Performance Tuning

```bash
# Parallel document processing
MAX_PARALLEL_DOCUMENTS=4

# Stage retry attempts
MAX_STAGE_RETRIES=3

# Enable optimized pipeline routing
ENABLE_OPTIMIZED_PIPELINE=true
OPTIMIZATION_ROLLOUT_PCT=50
```

## Troubleshooting

### Application Won't Start
```bash
# Check Python version
python3 --version  # Should be 3.12+

# Verify dependencies
pip install -r requirements.txt

# Check database
rm -f mortgage-lite.db
python3 scripts/load_demo.py
```

### Ollama Connection Failed
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Check model availability
ollama list
```

### Pipeline Hangs
```bash
# Check agent status in UI
# Navigate to Dashboard → Agents

# Check logs
tail -f logs/mortgage-lite.log

# Reset application status
# In UI: Applications → Select app → Reset Pipeline
```

### Claude CLI Not Found
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-cli

# Or use API directly
ANTHROPIC_API_KEY=your_key_here
```

## Next Steps

- Read the [Architecture Guide](./architecture.md) to understand system design
- Explore the [API Reference](./api-reference.md) for integration
- Check [Deployment Guide](./deployment.md) for production setup

## Support

For additional help:
- Check the [Troubleshooting Guide](../internal/troubleshooting.md)
- Review [Development Guide](../internal/development.md)
- Open an issue in the project repository
