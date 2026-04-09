# AgentX Documentation

Welcome to the AgentX documentation. AgentX is an AI Assistant Management Platform for Kubernetes.

## What is AgentX?

AgentX enables you to create, manage, and share AI assistants with your team. Deploy assistants in Kubernetes with a modern web interface and comprehensive API.

## Documentation

### For Users

- **[Overview](./overview.md)** - What AgentX is and what it can do
- **[Getting Started](./getting-started.md)** - Installation and first steps
- **[User Guide](./user-guide.md)** - How to use all features
- **[API Reference](./api-reference.md)** - REST API documentation

### Quick Start

```bash
# Install dependencies
uv sync && cd frontend && npm install

# Start development servers
task dev

# Access at http://localhost:5173
```

## Key Features

- **Easy Management**: Create, start, stop, and monitor AI assistants
- **Collaboration**: Share assistants with team members
- **Templates**: Reuse configurations across projects
- **Real-time**: Live updates and log streaming
- **Kubernetes Native**: Deploys as StatefulSets with persistent storage

## Need Help?

- **GitHub**: [dkubeio/agentx](https://github.com/dkubeio/agentx)
- **Issues**: [Report bugs or request features](https://github.com/dkubeio/agentx/issues)
- **API Docs**: Interactive docs at `/docs` endpoint

---

**Get Started**: Follow the [Getting Started Guide](./getting-started.md) to install AgentX.
