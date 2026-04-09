# Deployment Guide

This guide covers production deployment of Mortgage-Lite on various platforms.

## Prerequisites

### Required
- **Kubernetes 1.24+** (for Kubernetes deployment)
- **Helm 3.0+** (for Helm chart deployment)
- **PostgreSQL 14+** (for production database)
- **Docker 20.10+** (for container builds)

### Recommended
- **GPU nodes** for Ollama (NVIDIA T4 or better)
- **Persistent storage** (100GB+ for documents)
- **Load balancer** (for high availability)
- **Monitoring stack** (Prometheus + Grafana)

## Deployment Options

### 1. Docker Compose (Simple Production)

#### docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: mortgage_lite
      POSTGRES_USER: mortgage
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  mortgage-lite:
    image: ghcr.io/dkubeio/mortgage-lite:latest
    environment:
      DATABASE_URL: postgresql+asyncpg://mortgage:${DB_PASSWORD}@postgres:5432/mortgage_lite
      OLLAMA_BASE_URL: http://ollama:11434
      OLLAMA_MODEL: qwen3.5:35b
      CLAUDE_MODEL: sonnet
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      ANONYMIZATION_ENABLED: "true"
    volumes:
      - uploads:/app/uploads
    ports:
      - "5300:5300"
    depends_on:
      - postgres
      - ollama
    restart: unless-stopped

volumes:
  postgres_data:
  ollama_data:
  uploads:
```

#### Deploy
```bash
# Set environment variables
export DB_PASSWORD=your_secure_password
export ANTHROPIC_API_KEY=your_api_key

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f mortgage-lite

# Pull Ollama model
docker-compose exec ollama ollama pull qwen3.5:35b
```

### 2. Kubernetes with Helm

#### Add Helm Repository
```bash
helm repo add dkubeio https://dkubeio.github.io/helm-charts
helm repo update
```

#### Create values.yaml
```yaml
# values.yaml
replicaCount: 3

image:
  repository: ghcr.io/dkubeio/mortgage-lite
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 5300

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: mortgage-lite.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: mortgage-lite-tls
      hosts:
        - mortgage-lite.example.com

env:
  DATABASE_URL: postgresql+asyncpg://mortgage:password@postgres-service:5432/mortgage_lite
  OLLAMA_BASE_URL: http://ollama-service:11434
  OLLAMA_MODEL: qwen3.5:35b
  CLAUDE_MODEL: sonnet
  ANONYMIZATION_ENABLED: "true"
  DKUBEX_BASE_PATH: ""

secrets:
  ANTHROPIC_API_KEY: your_api_key_here

persistence:
  enabled: true
  storageClass: standard
  size: 100Gi

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

postgresql:
  enabled: true
  auth:
    username: mortgage
    password: secure_password
    database: mortgage_lite
  primary:
    persistence:
      enabled: true
      size: 50Gi

ollama:
  enabled: true
  image: ollama/ollama:latest
  service:
    port: 11434
  resources:
    limits:
      nvidia.com/gpu: 1
      memory: 32Gi
    requests:
      nvidia.com/gpu: 1
      memory: 16Gi
  nodeSelector:
    gpu: "true"
  persistence:
    enabled: true
    size: 200Gi
```

#### Install
```bash
# Create namespace
kubectl create namespace mortgage-lite

# Install with Helm
helm install mortgage-lite dkubeio/mortgage-lite \
  --namespace mortgage-lite \
  --values values.yaml

# Check status
kubectl get pods -n mortgage-lite
kubectl get svc -n mortgage-lite
kubectl get ingress -n mortgage-lite

# View logs
kubectl logs -f deployment/mortgage-lite -n mortgage-lite
```

#### Upgrade
```bash
# Update values.yaml, then:
helm upgrade mortgage-lite dkubeio/mortgage-lite \
  --namespace mortgage-lite \
  --values values.yaml

# Rollback if needed
helm rollback mortgage-lite -n mortgage-lite
```

### 3. DKubeX Platform Deployment

#### Create Application Manifest
```yaml
# mortgage-lite-app.yaml
apiVersion: dkube.io/v1
kind: Application
metadata:
  name: mortgage-lite
  namespace: default
spec:
  image: ghcr.io/dkubeio/mortgage-lite:latest
  replicas: 3
  port: 5300
  basePath: /mortgage-lite
  
  env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: mortgage-lite-secrets
          key: database-url
    - name: OLLAMA_BASE_URL
      value: http://ollama-service:11434
    - name: DKUBEX_BASE_PATH
      value: /mortgage-lite
    - name: ANONYMIZATION_ENABLED
      value: "true"
  
  resources:
    limits:
      cpu: 2
      memory: 4Gi
    requests:
      cpu: 1
      memory: 2Gi
  
  persistence:
    - name: uploads
      mountPath: /app/uploads
      size: 100Gi
  
  auth:
    enabled: true
    roles:
      - admin
      - underwriter
      - viewer
```

#### Deploy
```bash
# Apply manifest
kubectl apply -f mortgage-lite-app.yaml

# Check status
dkubex app status mortgage-lite

# Access via DKubeX UI
# URL: https://dkubex.example.com/mortgage-lite
```

## Database Setup

### PostgreSQL Configuration

#### Create Database
```sql
CREATE DATABASE mortgage_lite;
CREATE USER mortgage WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE mortgage_lite TO mortgage;
```

#### Connection String
```bash
# For asyncpg (recommended)
DATABASE_URL=postgresql+asyncpg://mortgage:password@postgres-host:5432/mortgage_lite

# For psycopg2
DATABASE_URL=postgresql://mortgage:password@postgres-host:5432/mortgage_lite
```

#### Performance Tuning
```sql
-- postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
max_connections = 200
```

### Database Migrations

Mortgage-Lite uses SQLAlchemy with automatic table creation. For production, consider using Alembic for migrations:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init migrations

# Generate migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

## Ollama Setup

### Pull Required Models
```bash
# On Ollama host/container
ollama pull qwen3.5:35b
ollama pull nemotron:70b  # Optional alternative
ollama pull llama3.1:70b  # Optional alternative

# Verify models
ollama list
```

### GPU Configuration

#### NVIDIA GPU
```yaml
# Kubernetes nodeSelector
nodeSelector:
  gpu: "true"

# Resource limits
resources:
  limits:
    nvidia.com/gpu: 1
```

#### AMD GPU
```yaml
resources:
  limits:
    amd.com/gpu: 1
```

### Performance Tuning
```bash
# Set Ollama environment variables
OLLAMA_NUM_PARALLEL=4
OLLAMA_MAX_LOADED_MODELS=2
OLLAMA_FLASH_ATTENTION=1
```

## Storage Configuration

### Persistent Volumes

#### Local Storage (Development)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mortgage-lite-uploads
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data/mortgage-lite
```

#### NFS Storage (Production)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mortgage-lite-uploads
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: nfs-server.example.com
    path: /exports/mortgage-lite
```

#### Cloud Storage (AWS EBS)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mortgage-lite-uploads
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    volumeID: vol-0123456789abcdef
    fsType: ext4
```

## Security Configuration

### Secrets Management

#### Kubernetes Secrets
```bash
# Create secrets
kubectl create secret generic mortgage-lite-secrets \
  --from-literal=database-url='postgresql+asyncpg://...' \
  --from-literal=anthropic-api-key='sk-...' \
  --from-literal=openai-api-key='sk-...' \
  -n mortgage-lite

# Use in deployment
env:
  - name: ANTHROPIC_API_KEY
    valueFrom:
      secretKeyRef:
        name: mortgage-lite-secrets
        key: anthropic-api-key
```

#### External Secrets Operator
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: mortgage-lite-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: mortgage-lite-secrets
  data:
    - secretKey: anthropic-api-key
      remoteRef:
        key: mortgage-lite/anthropic-api-key
```

### TLS/SSL Configuration

#### Cert-Manager
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: mortgage-lite-tls
spec:
  secretName: mortgage-lite-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - mortgage-lite.example.com
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mortgage-lite-network-policy
spec:
  podSelector:
    matchLabels:
      app: mortgage-lite
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 5300
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: ollama
      ports:
        - protocol: TCP
          port: 11434
```

## Monitoring & Observability

### Prometheus Metrics

Mortgage-Lite exposes metrics at `/metrics`:

```yaml
# ServiceMonitor for Prometheus Operator
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: mortgage-lite
spec:
  selector:
    matchLabels:
      app: mortgage-lite
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

### Grafana Dashboard

Import the provided Grafana dashboard:
- Dashboard ID: TBD
- Metrics include:
  - Application throughput
  - Agent performance
  - Pipeline latency
  - Error rates
  - Cost tracking

### Logging

#### Structured Logging
```python
# Configure in config.py
LOGGING_LEVEL=INFO
LOGGING_FORMAT=json
```

#### Log Aggregation (ELK Stack)
```yaml
# Filebeat sidecar
- name: filebeat
  image: docker.elastic.co/beats/filebeat:8.0.0
  volumeMounts:
    - name: logs
      mountPath: /var/log/mortgage-lite
```

## High Availability

### Multi-Region Deployment

```yaml
# Region 1
apiVersion: v1
kind: Service
metadata:
  name: mortgage-lite-us-east
spec:
  type: LoadBalancer
  selector:
    app: mortgage-lite
    region: us-east

# Region 2
apiVersion: v1
kind: Service
metadata:
  name: mortgage-lite-us-west
spec:
  type: LoadBalancer
  selector:
    app: mortgage-lite
    region: us-west
```

### Database Replication

```yaml
# PostgreSQL with streaming replication
postgresql:
  replication:
    enabled: true
    numSynchronousReplicas: 1
    synchronousCommit: "on"
  readReplicas:
    replicaCount: 2
```

### Load Balancing

```yaml
# NGINX Ingress with load balancing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mortgage-lite
  annotations:
    nginx.ingress.kubernetes.io/load-balance: "round_robin"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
spec:
  rules:
    - host: mortgage-lite.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: mortgage-lite
                port:
                  number: 5300
```

## Backup & Recovery

### Database Backups

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR=/backups/mortgage-lite
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump -h postgres-host -U mortgage mortgage_lite | \
  gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /app/uploads

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -mtime +30 -delete
```

### Restore Procedure

```bash
# Restore database
gunzip -c db_backup_20240115_120000.sql.gz | \
  psql -h postgres-host -U mortgage mortgage_lite

# Restore uploads
tar -xzf uploads_20240115_120000.tar.gz -C /app/uploads
```

## Performance Optimization

### Application Tuning

```bash
# Environment variables
UVICORN_WORKERS=4
UVICORN_WORKER_CLASS=uvicorn.workers.UvicornWorker
MAX_PARALLEL_DOCUMENTS=4
ENABLE_OPTIMIZED_PIPELINE=true
```

### Database Connection Pooling

```python
# config.py
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
```

### Caching

```yaml
# Redis for caching
redis:
  enabled: true
  master:
    persistence:
      enabled: true
      size: 10Gi
```

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check logs
kubectl logs deployment/mortgage-lite -n mortgage-lite

# Check events
kubectl get events -n mortgage-lite

# Verify secrets
kubectl get secrets -n mortgage-lite
```

#### Database Connection Failed
```bash
# Test connection
kubectl run -it --rm debug --image=postgres:14 --restart=Never -- \
  psql -h postgres-service -U mortgage -d mortgage_lite

# Check service
kubectl get svc postgres-service -n mortgage-lite
```

#### Ollama Not Responding
```bash
# Check Ollama pod
kubectl logs deployment/ollama -n mortgage-lite

# Test Ollama API
kubectl exec -it deployment/mortgage-lite -n mortgage-lite -- \
  curl http://ollama-service:11434/api/tags
```

### Health Checks

```yaml
# Liveness probe
livenessProbe:
  httpGet:
    path: /health
    port: 5300
  initialDelaySeconds: 30
  periodSeconds: 10

# Readiness probe
readinessProbe:
  httpGet:
    path: /health
    port: 5300
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Maintenance

### Rolling Updates

```bash
# Update image
kubectl set image deployment/mortgage-lite \
  mortgage-lite=ghcr.io/dkubeio/mortgage-lite:v2.0.0 \
  -n mortgage-lite

# Monitor rollout
kubectl rollout status deployment/mortgage-lite -n mortgage-lite

# Rollback if needed
kubectl rollout undo deployment/mortgage-lite -n mortgage-lite
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment/mortgage-lite --replicas=5 -n mortgage-lite

# Autoscaling
kubectl autoscale deployment/mortgage-lite \
  --min=3 --max=10 --cpu-percent=70 \
  -n mortgage-lite
```

## Cost Optimization

### Resource Right-Sizing

Monitor actual usage and adjust:
```yaml
resources:
  requests:
    cpu: 500m      # Start conservative
    memory: 1Gi
  limits:
    cpu: 2000m     # Allow bursting
    memory: 4Gi
```

### Spot Instances (AWS)

```yaml
nodeSelector:
  node.kubernetes.io/instance-type: spot
tolerations:
  - key: spot
    operator: Equal
    value: "true"
    effect: NoSchedule
```

## Compliance & Audit

### Audit Logging

Enable comprehensive audit logging:
```bash
AUDIT_LOGGING_ENABLED=true
AUDIT_LOG_RETENTION_DAYS=90
```

### Data Retention

```sql
-- Cleanup old data
DELETE FROM audit_log WHERE created_at < NOW() - INTERVAL '90 days';
DELETE FROM token_usage WHERE created_at < NOW() - INTERVAL '30 days';
```

## Support

For deployment support:
- Review [Architecture Guide](./architecture.md)
- Check [Troubleshooting Guide](../internal/troubleshooting.md)
- Contact platform team
