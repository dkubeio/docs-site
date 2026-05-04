# Getting Started with AgentX

AgentX is an AI Assistant Management Platform for Kubernetes that enables you to create, manage, and share AI assistants with ease.

## Quick Start

### Prerequisites

Before you begin, ensure you have:

- **Python 3.12+** installed
- **Node.js 18+** installed
- **uv** package manager (recommended) or pip
- **Docker** (for building images)
- **Kubernetes cluster** (for production deployment)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/dkubeio/agentx.git
cd agentx
```

#### 2. Install Dependencies

Using uv (recommended):
```bash
# Install Python dependencies
uv sync

# Install frontend dependencies
cd frontend && npm install
```

Using pip:
```bash
# Install Python dependencies
pip install -e .

# Install frontend dependencies
cd frontend && npm install
```

#### 3. Configure Environment

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./agentx.db

# Authentication Mode
# Options: local-admin (development) or oauth2-proxy (production)
AUTHENTICATION_MODE=local-admin

# Security
SECRET_KEY=your-secret-key-change-in-production
```

#### 4. Initialize Database

```bash
cd backend
uv run alembic upgrade head
```

#### 5. Start Development Servers

**Option A: Using Task (recommended)**

```bash
task dev
```

**Option B: Manual Start**

Terminal 1 - Backend:
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

#### 6. Access the Application

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## First Steps

### Creating Your First Assistant

1. Open the AgentX UI at http://localhost:5173
2. Click the **"Create Assistant"** button
3. Fill in the assistant details:
   - **Name**: Give your assistant a unique name
   - **Description**: Describe what your assistant does
   - **Configuration**: Add any custom configuration (JSON format)
4. Click **"Create"** to deploy your assistant

Your assistant will be automatically started and deployed as a Kubernetes StatefulSet (in production) or a local process (in development).

### Managing Assistants

Once created, you can:

- **Start/Stop**: Control assistant lifecycle
- **Restart**: Restart a running assistant
- **View Logs**: Stream real-time logs from your assistant
- **Update**: Modify assistant configuration
- **Delete**: Remove an assistant and its resources

### Sharing Assistants

To share an assistant with other users:

1. Navigate to your assistant
2. Click the **"Share"** button
3. Search for users by username or email
4. Select permission level:
   - **Read**: View-only access
   - **Write**: Can modify the assistant
5. Click **"Share"**

Shared assistants appear in the **"Shared with Me"** tab for recipients.

### Using Templates

Templates allow you to reuse assistant configurations:

#### Publishing a Template

1. Open an existing assistant
2. Click **"Publish as Template"**
3. Provide template details:
   - **Name**: Template name
   - **Description**: What this template does
   - **Tags**: Categorize your template
   - **Version**: Semantic version (e.g., 1.0.0)
4. Click **"Publish"**

#### Deploying from Template

1. Navigate to the **"Templates"** tab
2. Browse available templates
3. Click **"Deploy"** on a template
4. Provide a name for your new assistant
5. Click **"Create"**

## Development Workflow

### Project Structure

```
agentx/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core functionality
│   │   ├── crud/     # Database operations
│   │   ├── models/   # Database models
│   │   └── schemas/  # API schemas
│   └── alembic/      # Database migrations
├── frontend/         # React frontend
│   └── src/
│       ├── components/
│       └── lib/
└── helm/            # Kubernetes deployment
```

### Running Tests

```bash
# Backend tests
uv run pytest backend/tests/

# Frontend tests
cd frontend && npm test
```

### Building for Production

```bash
# Build Docker image
docker build -t agentx:latest .

# Build assistant runtime image
docker build -t agentx-assistant:latest -f assistant/Dockerfile assistant/
```

## Kubernetes Deployment

### Using Helm

```bash
# Install AgentX
helm install agentx ./helm/agentx \
  --namespace dkubex-apps \
  --create-namespace \
  --set database.db_url=postgresql://user:password@postgres/agentx \
  --set hostname=your-domain.com
```

### Configuration Options

Key Helm values:

```yaml
# Image configuration
image:
  repository: ghcr.io/dkubeio/agentx
  tag: "latest"

# Database
database:
  enabled: true
  db_url: postgresql://user:password@host/agentx

# Authentication
authentication:
  mode: oauth2-proxy  # or local-admin

# Resources
resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

## Authentication

### Local Development (local-admin mode)

In development, AgentX uses a default admin user:
- **Username**: default
- **Email**: admin@example.com
- **Role**: admin

No authentication is required.

### Production (oauth2-proxy mode)

In Kubernetes environments, AgentX integrates with OAuth2 Proxy:

1. OAuth2 Proxy authenticates users
2. Passes user information via headers:
   - `X-Auth-Request-User`: Username
   - `X-Auth-Request-Email`: Email
   - `X-Auth-Request-Groups`: User groups
   - `X-Auth-Request-User-Namespace`: Kubernetes namespace
3. AgentX automatically creates user records on first access

## Troubleshooting

### Common Issues

**Issue**: Database connection errors
```bash
# Solution: Check DATABASE_URL in .env
# For SQLite (development):
DATABASE_URL=sqlite:///./agentx.db

# For PostgreSQL (production):
DATABASE_URL=postgresql://user:password@localhost/agentx
```

**Issue**: Frontend can't connect to backend
```bash
# Solution: Ensure backend is running on port 8000
# Check frontend proxy configuration in vite.config.ts
```

**Issue**: Kubernetes resources not created
```bash
# Solution: Verify kubectl access
kubectl get pods -n dkubex-apps

# Check assistant logs
kubectl logs -n dkubex-apps <pod-name>
```

**Issue**: Authentication errors in Kubernetes
```bash
# Solution: Verify OAuth2 Proxy headers
# Check authentication mode setting
AUTHENTICATION_MODE=oauth2-proxy
```

### Getting Help

- **Documentation**: [Full Documentation](https://dkubeio.github.io/docs-site/components/agentx/)
- **API Docs**: http://localhost:8000/docs (when running locally)
- **Issues**: [GitHub Issues](https://github.com/dkubeio/agentx/issues)

## Next Steps

- Explore the [API Reference](./api-reference.md) for detailed endpoint documentation
- Review [User Guide](./user-guide.md) for advanced features
- Check the [Overview](./overview.md) to learn more about AgentX capabilities
