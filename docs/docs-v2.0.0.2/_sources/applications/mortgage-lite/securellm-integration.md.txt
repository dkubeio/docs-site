# SecureLLM Integration Guide

This guide explains how to integrate and configure SecureLLM as a local inference provider in Mortgage-Lite.

## Overview

SecureLLM is a local inference server that provides an OpenAI-compatible chat completions API. It allows you to run AI models on your own infrastructure while maintaining full data privacy and control.

### Benefits

- **Privacy**: All data stays on your infrastructure
- **Control**: Full control over model selection and configuration
- **Cost**: No per-token cloud API costs
- **Compliance**: Meet data residency requirements
- **Performance**: Low latency for local deployments

## Configuration

SecureLLM can be configured in three ways:

### 1. Environment Variables (.env)

```bash
# SecureLLM Configuration (Kubernetes same namespace: dkubex-apps)
SECURELLM_BASE_URL=http://securellm/securellm/v1
SECURELLM_API_KEY=your_api_key_here

# Note: Models are discovered automatically from the gateway
# No need to specify SECURELLM_MODEL
```

### 2. Helm Values (values.yaml)

```yaml
env:
  - name: SECURELLM_BASE_URL
    value: "http://securellm/securellm/v1"
  - name: SECURELLM_API_KEY
    value: "your_api_key_here"
  # Models are auto-discovered from the gateway
```

### 3. UI Settings Page

Navigate to **Settings** in the Mortgage-Lite UI and configure:

- **SecureLLM Base URL**: The endpoint URL (e.g., `http://securellm/securellm/v1` for k8s same namespace)
- **SecureLLM API Key**: Your API key (optional, depending on your setup)
- **Default AI Mode**: Select "SecureLLM (Local Inference)" to use it as default

**Note**: Available models are discovered automatically from the SecureLLM gateway. You don't need to configure specific model names.

## API Endpoint

SecureLLM uses the OpenAI-compatible chat completions endpoint:

```
POST {SECURELLM_BASE_URL}/chat/completions
```

### Request Format

```json
{
  "model": "default",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Analyze this mortgage application..."
    }
  ],
  "stream": false
}
```

### Response Format

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Based on the application..."
      }
    }
  ]
}
```

## Usage in Agents

SecureLLM can be used by any agent in the pipeline. Here's how to configure agents to use SecureLLM:

### Option 1: Set as Default AI Mode

In the UI Settings, set **Default AI Mode** to "SecureLLM (Local Inference)". All agents will use SecureLLM by default.

### Option 2: Programmatic Selection

In agent code, specify the provider:

```python
from app.services.ai import chat

# Use SecureLLM explicitly
result = await chat(
    system_prompt="You are Ana, the mortgage analyzer...",
    messages=[{"role": "user", "content": prompt}],
    provider="securellm"
)
```

### Option 3: Call Model Dispatcher

```python
from app.services.ai import call_model

result = await call_model(
    provider="securellm",
    model="default",
    prompt="Analyze this application...",
    timeout=300
)
```

## Agent-Specific Usage

### Ana (Analyzer Agent)

Ana processes raw PII data locally. SecureLLM is ideal for this:

```python
# In ana.py
async def process(self, application: Application, db: AsyncSession) -> str:
    # Build context with raw data
    context = await self._build_context(application, db)
    
    # Use SecureLLM for privacy-safe local processing
    result = await chat(
        system_prompt=self._instructions(application),
        messages=[{"role": "user", "content": context}],
        provider="securellm"
    )
    
    return result
```

### Claire (Compliance Agent)

While Claire typically uses Claude for compliance, you can use SecureLLM for fully local processing:

```python
# In claire.py
async def process(self, application: Application, db: AsyncSession) -> str:
    # Get anonymized data
    anonymized = await self._get_anonymized_data(application, db)
    
    # Use SecureLLM instead of Claude
    result = await chat(
        system_prompt=self._instructions(application),
        messages=[{"role": "user", "content": anonymized}],
        provider="securellm"
    )
    
    return result
```

## Authentication

SecureLLM supports Bearer token authentication:

```bash
# Set API key in environment
SECURELLM_API_KEY=your_secret_key
```

The API key is automatically included in requests:

```http
POST /securellm/v1/chat/completions
Authorization: Bearer your_secret_key
Content-Type: application/json
```

If your SecureLLM deployment doesn't require authentication, leave `SECURELLM_API_KEY` empty.

## Network Configuration

### Local Deployment

If SecureLLM is on the same machine:

```bash
SECURELLM_BASE_URL=http://localhost:8000/v1
```

### Remote Deployment (External Access)

If SecureLLM is accessed via external IP (not recommended for production):

```bash
SECURELLM_BASE_URL=http://external-ip/securellm/v1
```

### Kubernetes Cross-Namespace

If SecureLLM is in the same namespace (`dkubex-apps`):

```bash
SECURELLM_BASE_URL=http://securellm/securellm/v1
```

For same-namespace services, use just the service name. For cross-namespace: `<service-name>.<namespace>.svc.cluster.local`

### Kubernetes Deployment

If SecureLLM is deployed in the same Kubernetes cluster:

```yaml
env:
  - name: SECURELLM_BASE_URL
    value: "http://securellm/securellm/v1"
```

## Dynamic Model Discovery

Mortgage-Lite automatically discovers available models from the SecureLLM gateway at runtime. This means:

- **No manual configuration needed**: Models are detected automatically
- **Real-time availability**: Checks for model availability before each LLM call
- **Intelligent fallback**: If a model isn't available in SecureLLM, falls back to Ollama
- **Flexible matching**: Supports various model naming conventions

### How It Works

1. **Model Discovery**: When Ana or Rex agents need an LLM, they first query SecureLLM's `/models` endpoint
2. **Availability Check**: The system checks if the required model (e.g., `qwen3.5:35b`) is available
3. **Flexible Matching**: Supports exact and partial matches (e.g., `qwen3.5:35b` matches `shared--qwen3-5-35b`)
4. **Automatic Fallback**: If model not found or request fails, automatically falls back to Ollama

### Supported Models

Any model available in your SecureLLM deployment will be automatically detected. Common models:
- Qwen family: `qwen3.5:35b`, `qwen2-vl`, `qwen-72b`
- Llama family: `llama-3-70b`, `llama3.1:70b`
- Mistral family: `mistral-7b`, `mistral-nemo`
- Gemma family: `gemma-3-1b`, `gemma-7b`

## Performance Tuning

### Timeout Configuration

Adjust timeout for large models or complex prompts:

```python
result = await chat(
    system_prompt=prompt,
    messages=messages,
    provider="securellm",
    timeout=600  # 10 minutes
)
```

### Concurrent Requests

SecureLLM can handle multiple concurrent requests. Configure in `config.py`:

```python
max_parallel_documents: int = 4  # Process 4 documents concurrently
```

## Monitoring

### Health Check

Test SecureLLM connectivity:

```bash
# From within the same namespace
curl -X POST http://securellm/securellm/v1/chat/completions \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "default",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

### Token Usage Tracking

Mortgage-Lite tracks token usage for all providers including SecureLLM:

```sql
SELECT * FROM token_usage WHERE provider = 'securellm';
```

View in UI: **Metrics** → **Agent Performance**

## Troubleshooting

### Connection Refused

```
RuntimeError: SecureLLM returned 000: Connection refused
```

**Solutions**:
- Verify SecureLLM is running: `curl http://securellm/securellm/v1/health`
- Check firewall rules
- Verify URL is correct (include `/v1` in base URL)

### Authentication Failed

```
RuntimeError: SecureLLM returned 401: Unauthorized
```

**Solutions**:
- Verify API key is correct
- Check if API key is required (some deployments don't require auth)
- Ensure `Authorization: Bearer` header format is correct

### Model Not Found

```
RuntimeError: SecureLLM returned 404: Model not found
```

**Solutions**:
- Check available models in SecureLLM
- Use `default` model if unsure
- Verify model name matches SecureLLM configuration

### Timeout Errors

```
TimeoutError: SecureLLM request timed out after 300s
```

**Solutions**:
- Increase timeout: `timeout=600`
- Use smaller model
- Reduce prompt size
- Check SecureLLM server resources

## Migration from Ollama

If you're currently using Ollama and want to switch to SecureLLM:

### 1. Update Configuration

```bash
# Old (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:35b

# New (SecureLLM - Kubernetes same namespace)
SECURELLM_BASE_URL=http://securellm/securellm/v1
SECURELLM_API_KEY=your_key
SECURELLM_MODEL=qwen-72b
```

### 2. Update Default AI Mode

In UI Settings:
- Change **Default AI Mode** from "Local (Ollama)" to "SecureLLM (Local Inference)"

### 3. Test

Run a test application through the pipeline to verify SecureLLM is working correctly.

## Best Practices

### 1. Use for Privacy-Sensitive Data

SecureLLM is ideal for processing raw PII data in Ana agent:
- All data stays on your infrastructure
- No data sent to cloud providers
- Full audit trail

### 2. Model Selection

Choose appropriate model size:
- **Small models (7B-13B)**: Fast, lower resource usage, good for simple tasks
- **Medium models (30B-40B)**: Balanced performance and quality
- **Large models (70B+)**: Best quality, higher resource requirements

### 3. Caching

Enable response caching for repeated queries:
- Reduces inference time
- Lowers resource usage
- Improves user experience

### 4. Load Balancing

For high-volume deployments:
- Deploy multiple SecureLLM instances
- Use load balancer
- Configure in Kubernetes with multiple replicas

## Security Considerations

### 1. API Key Management

- Store API keys in Kubernetes secrets
- Never commit API keys to version control
- Rotate keys regularly

### 2. Network Security

- Use TLS/SSL for production deployments
- Restrict network access to SecureLLM
- Use VPN or private network

### 3. Data Privacy

- SecureLLM processes data locally
- No data leaves your infrastructure
- Compliant with GDPR, HIPAA, etc.

## Example Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  securellm:
    image: securellm/server:latest
    ports:
      - "8000:8000"
    environment:
      - MODEL_NAME=qwen-72b
      - API_KEY=your_secret_key
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  mortgage-lite:
    image: mortgage-lite:latest
    ports:
      - "5300:5300"
    environment:
      - SECURELLM_BASE_URL=http://securellm:8000/v1
      - SECURELLM_API_KEY=your_secret_key
      - SECURELLM_MODEL=qwen-72b
    depends_on:
      - securellm
```

### Kubernetes

```yaml
apiVersion: v1
kind: Service
metadata:
  name: securellm
spec:
  selector:
    app: securellm
  ports:
    - port: 8000
      targetPort: 8000

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: securellm
spec:
  replicas: 2
  selector:
    matchLabels:
      app: securellm
  template:
    metadata:
      labels:
        app: securellm
    spec:
      containers:
        - name: securellm
          image: securellm/server:latest
          ports:
            - containerPort: 8000
          env:
            - name: MODEL_NAME
              value: "qwen-72b"
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: securellm-secret
                  key: api-key
          resources:
            limits:
              nvidia.com/gpu: 1
```

## Support

For SecureLLM-specific issues:
- Check SecureLLM documentation
- Verify API endpoint is accessible
- Test with curl before integrating

For Mortgage-Lite integration issues:
- Check logs: `tail -f logs/mortgage-lite.log`
- Verify configuration in UI Settings
- Test with different AI modes to isolate issue

## Summary

SecureLLM integration provides:
- ✅ Full data privacy and control
- ✅ OpenAI-compatible API
- ✅ Configurable via .env, Helm, and UI
- ✅ Support for multiple models
- ✅ Production-ready deployment options

Configure SecureLLM in Settings and start processing mortgage applications with complete data privacy!
