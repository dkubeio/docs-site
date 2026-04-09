# User Guide

This guide covers advanced features and best practices for using AgentX effectively.

## Managing Assistants

### Creating Assistants

#### From Scratch

1. Click **"Create Assistant"** button
2. Fill in the form:
   - **Name**: Unique identifier (lowercase, alphanumeric, hyphens)
   - **Description**: What your assistant does
   - **Configuration**: JSON object with custom settings

Example configuration:
```json
{
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000,
  "system_prompt": "You are a helpful assistant"
}
```

3. Click **"Create"** to deploy

#### From Template

1. Navigate to **"Templates"** tab
2. Browse available templates
3. Click **"Deploy"** on desired template
4. Provide a unique name
5. Optionally modify description
6. Click **"Create"**

### Assistant Lifecycle

#### Starting an Assistant

- **Auto-start**: Assistants start automatically on creation
- **Manual start**: Click **"Start"** button on stopped assistant
- **Status**: Changes from "stopped" → "starting" → "running"

#### Stopping an Assistant

- Click **"Stop"** button on running assistant
- Kubernetes resources are deleted
- Database record and configuration preserved
- Can be restarted later

#### Restarting an Assistant

- Click **"Restart"** button on running assistant
- Performs stop + start sequence
- Useful for applying configuration changes
- Maintains same pod identity

#### Deleting an Assistant

- Click **"Delete"** button
- Confirms deletion
- Removes all Kubernetes resources
- Deletes database record
- **Warning**: This action cannot be undone

### Viewing Logs

1. Click on an assistant to open details
2. Click **"View Logs"** button
3. Real-time log stream appears
4. Logs update automatically
5. Click **"Close"** to stop streaming

**Log Features**:
- Real-time streaming via Server-Sent Events
- Automatic reconnection on disconnect
- Searchable and scrollable
- Timestamps included

### Updating Configuration

1. Open assistant details
2. Click **"Edit"** button
3. Modify fields:
   - Name (must remain unique)
   - Description
   - Configuration JSON
4. Click **"Save"**
5. Restart assistant to apply changes

## Collaboration Features

### Sharing Assistants

#### Share with Users

1. Open assistant details
2. Click **"Share"** button
3. Search for users by username or email
4. Select users to share with
5. Choose permission level:
   - **Read**: View-only access
   - **Write**: Can modify assistant
6. Click **"Share"**

#### Managing Shares

**View Shares**:
- Open assistant details
- Click **"Manage Shares"** tab
- See list of users with access

**Update Permissions**:
- Click **"Edit"** next to a share
- Change permission level
- Click **"Save"**

**Revoke Access**:
- Click **"Remove"** next to a share
- Confirm revocation
- User loses access immediately

### Accessing Shared Assistants

**View Shared Assistants**:
1. Navigate to **"Shared with Me"** tab
2. See all assistants shared with you
3. Permission level displayed for each

**Using Shared Assistants**:
- **Read permission**: View details, view logs
- **Write permission**: Edit configuration, restart, stop/start

**Limitations**:
- Cannot delete shared assistants (owner only)
- Cannot share with others (owner only)
- Cannot publish as template (owner only)

### Pinning Assistants

Pin frequently used assistants for quick access:

**Pin an Assistant**:
1. Click **"Pin"** icon on assistant card
2. Assistant appears in pinned section
3. Works for owned and shared assistants

**Unpin an Assistant**:
1. Click **"Unpin"** icon
2. Assistant removed from pinned section
3. Still accessible in main list

**Pinned Section**:
- Appears at top of assistant list
- Persists across sessions
- Personal to each user

## Templates

### Publishing Templates

Convert your assistant configuration into a reusable template:

1. Open a working assistant
2. Click **"Publish as Template"**
3. Fill in template details:
   - **Name**: Template name
   - **Description**: What it does
   - **Tags**: Categorization (e.g., "ai", "gpt-4")
   - **Version**: Semantic version (1.0.0)
   - **Metadata**: Additional info (JSON)

Example metadata:
```json
{
  "author": "John Doe",
  "category": "AI Assistants",
  "use_case": "Code generation",
  "requirements": ["GPU", "High memory"]
}
```

4. Click **"Publish"**

### Template Versioning

Create multiple versions of a template:

**Create New Version**:
1. Open template details
2. Click **"Create Version"**
3. Provide:
   - **Version**: Semantic version (1.1.0)
   - **Configuration**: Updated config
   - **Changelog**: What changed
4. Click **"Create"**

**Deprecate Version**:
1. Open template details
2. Click **"Versions"** tab
3. Click **"Deprecate"** on old version
4. Provide deprecation message
5. Users see warning when deploying

**Version Selection**:
- Latest version deployed by default
- Can select specific version when deploying
- Deprecated versions show warning

### Browsing Templates

**Search Templates**:
- Use search box to filter by name/description
- Filter by tags
- Sort by usage count or date

**Template Details**:
- Click on template to view details
- See configuration preview
- View version history
- Check usage count
- Read metadata

## Admin Features

### Admin Dashboard

Access via **"Admin"** tab (admin users only):

**System Overview**:
- Total users count
- Total assistants count
- Running/stopped/error counts
- System health status
- Uptime information

**Service Status**:
- Database health
- Kubernetes status
- API health

### User Management

**List Users**:
1. Navigate to **"Admin"** → **"Users"**
2. See all registered users
3. Search by username or email

**View User Details**:
1. Click on a user
2. See user information
3. View user's assistants

**Create User**:
1. Click **"Create User"**
2. Provide:
   - Username
   - Email
   - Role (user/admin)
   - Namespace
3. Click **"Create"**

**Update User Role**:
1. Open user details
2. Click **"Edit"**
3. Change role
4. Click **"Save"**
5. Action logged in audit log

**Delete User**:
1. Open user details
2. Click **"Delete"**
3. Confirm deletion
4. User and their assistants removed

### Assistant Management

**View All Assistants**:
1. Navigate to **"Admin"** → **"Assistants"**
2. See assistants across all users
3. Filter by status or owner
4. Search by name

**Stop Any Assistant**:
1. Find assistant in list
2. Click **"Stop"**
3. Confirm action
4. Action logged in audit log

**Delete Any Assistant**:
1. Find assistant in list
2. Click **"Delete"**
3. Confirm deletion
4. Action logged in audit log

### Monitoring

**Pod Metrics**:
1. Navigate to **"Admin"** → **"Metrics"**
2. View CPU and memory usage
3. See pod status
4. Identify resource-heavy assistants

**Audit Logs**:
1. Navigate to **"Admin"** → **"Audit Logs"**
2. View admin actions
3. Filter by action type
4. Search by resource ID or username

**Log Entries Include**:
- Timestamp
- Admin username
- Action performed
- Resource type and ID
- Additional details

## Best Practices

### Naming Conventions

**Assistants**:
- Use lowercase
- Use hyphens for spaces
- Be descriptive: `code-reviewer`, `data-analyzer`
- Avoid special characters

**Templates**:
- Use title case
- Be descriptive: "GPT-4 Code Assistant"
- Include version in name if needed

### Configuration Management

**Version Control**:
- Keep configuration in version control
- Document changes in description
- Use template versions for major changes

**Environment-Specific Config**:
- Use different assistants for dev/staging/prod
- Name accordingly: `my-assistant-dev`, `my-assistant-prod`

**Secrets**:
- Never hardcode API keys in configuration
- Use Kubernetes Secrets
- Reference secrets in configuration

### Resource Management

**Optimize Resources**:
- Stop assistants when not in use
- Monitor resource usage via admin panel
- Delete unused assistants

**Sharing Strategy**:
- Share with specific users, not everyone
- Use read permission for viewers
- Use write permission for collaborators
- Review shares periodically

### Template Strategy

**When to Create Templates**:
- Reusable configurations
- Standard setups for teams
- Common use cases
- Tested and validated configs

**Template Maintenance**:
- Update versions for improvements
- Deprecate old versions
- Document breaking changes
- Keep metadata current

## Troubleshooting

### Assistant Won't Start

**Check Status**:
- View assistant details
- Check error message
- View logs for details

**Common Issues**:
- Insufficient resources in namespace
- Invalid configuration
- Storage quota exceeded
- Network issues

**Solutions**:
- Contact admin for resource increase
- Validate configuration JSON
- Delete unused assistants
- Check Kubernetes cluster health

### Cannot Share Assistant

**Possible Causes**:
- User not found
- Already shared with user
- Trying to share with yourself

**Solutions**:
- Verify username/email
- Check existing shares
- Share with different user

### Template Deployment Fails

**Check**:
- Template configuration validity
- Namespace quotas
- Naming conflicts

**Solutions**:
- Choose different name
- Contact admin for quota increase
- Review template configuration

### Logs Not Streaming

**Troubleshooting**:
- Refresh page
- Check assistant status (must be running)
- Verify network connection
- Check browser console for errors

**Solutions**:
- Restart assistant
- Try different browser
- Contact admin if persists

## Keyboard Shortcuts

### Navigation

- **Tab**: Navigate between tabs
- **Arrow Keys**: Move between tabs
- **Home**: First tab
- **End**: Last tab

### Actions

- **Enter**: Activate focused button
- **Escape**: Close modal/dialog
- **Space**: Toggle checkbox/button

## Accessibility

AgentX is built with accessibility in mind:

- **Screen Reader Support**: ARIA labels and roles
- **Keyboard Navigation**: Full keyboard support
- **Focus Indicators**: Visible focus states
- **Color Contrast**: WCAG AA compliant
- **Responsive Design**: Works on all screen sizes

## Getting Help

### Documentation

- **Getting Started**: Quick start guide
- **API Reference**: Complete API documentation
- **Architecture**: System design details
- **Deployment**: Production deployment guide

### Support Channels

- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: https://dkubeio.github.io/docs-site/components/agentx/
- **API Docs**: http://localhost:8000/docs (local)

### Reporting Issues

When reporting issues, include:

1. **Description**: What went wrong
2. **Steps to Reproduce**: How to recreate
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happened
5. **Environment**: Browser, OS, AgentX version
6. **Logs**: Relevant error messages

## Tips and Tricks

### Efficient Workflow

1. **Pin frequently used assistants** for quick access
2. **Use templates** for common configurations
3. **Share assistants** instead of duplicating
4. **Monitor resources** via admin panel
5. **Stop unused assistants** to save resources

### Advanced Usage

**Bulk Operations**:
- Share with multiple users at once
- Create multiple assistants from same template
- Use API for automation

**Configuration Patterns**:
- Use environment variables in config
- Reference external resources
- Modular configuration structure

**Monitoring**:
- Set up alerts for assistant failures
- Monitor resource usage trends
- Review audit logs regularly

### Performance Optimization

**Frontend**:
- Use latest browser version
- Clear cache if experiencing issues
- Disable browser extensions if needed

**Backend**:
- Use pagination for large lists
- Filter results to reduce data transfer
- Close log streams when not needed

**Assistants**:
- Optimize configuration for performance
- Use appropriate resource limits
- Monitor and adjust based on usage
