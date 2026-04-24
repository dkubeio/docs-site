# AgentX Overview

AgentX is an AI Assistant Management Platform for Kubernetes that enables you to create, manage, and share AI assistants with ease.

## What is AgentX?

AgentX provides a comprehensive platform for deploying and managing AI assistants in Kubernetes environments. It features a modern web interface, robust API, and seamless integration with Kubernetes resources.

## Key Features

### Assistant Management
- **Create & Deploy**: Launch AI assistants with custom configurations
- **Lifecycle Control**: Start, stop, restart, and delete assistants
- **Real-time Logs**: Stream logs directly from running assistants
- **Status Monitoring**: Track assistant health and status

### Collaboration
- **Share Assistants**: Share with team members with granular permissions
- **Permission Levels**: Three-tier access control (VIEW, USE, MANAGE)
- **Pin Favorites**: Quick access to frequently used assistants
- **Shared with Me**: Easy discovery of assistants shared with you

### Templates
- **Reusable Configurations**: Publish assistant setups as templates
- **Version Control**: Manage multiple template versions
- **One-Click Deploy**: Create new assistants from templates instantly
- **Usage Tracking**: See how often templates are used

### Administration
- **User Management**: Create and manage user accounts
- **System Monitoring**: View resource usage and system health
- **Audit Logging**: Track administrative actions
- **Metrics Dashboard**: Monitor CPU and memory usage

## How It Works

```
1. Create Assistant → 2. Configure → 3. Deploy → 4. Use & Share
```

### 1. Create an Assistant
Choose to create from scratch or deploy from a template. Provide a name, description, and configuration.

### 2. Configure
Set up your assistant with custom parameters, model settings, and environment variables.

### 3. Deploy
AgentX automatically deploys your assistant as a Kubernetes StatefulSet with persistent storage.

### 4. Use & Share
Access your assistant, view logs, and share with team members as needed.

## Use Cases

### Development Teams
- Share development assistants across the team
- Standardize configurations with templates
- Track resource usage per assistant

### AI/ML Projects
- Deploy multiple assistant variants for testing
- Version control assistant configurations
- Collaborate on prompt engineering

### Enterprise
- Centralized assistant management
- Role-based access control
- Audit trail for compliance

## Technology Stack

- **Frontend**: React + TypeScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Orchestration**: Kubernetes
- **Assistant Interface**: OpenClaw gateway + in-browser Claude Code / OpenCode TUIs (ttyd)
- **Authentication**: OAuth2 Proxy

## Getting Started

Ready to start using AgentX? Check out our [Getting Started Guide](./getting-started.md) for installation and setup instructions.

## Need Help?

- **User Guide**: [Advanced features and best practices](./user-guide.md)
- **API Reference**: [Complete API documentation](./api-reference.md)
- **Support**: Open an issue on GitHub

## Quick Links

- [Getting Started](./getting-started.md) - Installation and setup
- [User Guide](./user-guide.md) - How to use AgentX
- [API Reference](./api-reference.md) - REST API documentation
