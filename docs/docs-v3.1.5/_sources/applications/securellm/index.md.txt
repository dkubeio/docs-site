# SecureLLM

SecureLLM is your organization's secure gateway to AI. Instead of everyone connecting directly to different AI services, all requests go through one central hub that your team controls. This means consistent access, cost tracking, and safety guardrails — without you needing to manage separate accounts or API keys for every AI provider.

## Key features

- **Central gateway** — Every AI request goes through one controlled hub instead of connecting to providers directly.
- **Single sign-on** — Log in automatically with your organization's existing credentials; no separate account or password.
- **API keys** — Create and revoke keys that let your scripts, tools, and IDE plugins talk to SecureLLM on your behalf.
- **Model browser** — Search and filter every model available to you, and copy its identifier for use in your code.
- **Usage tracking** — Review your request history with token counts, cost, latency, and any guardrail events.
- **Guardrails** — Automatic safety filters for sensitive content, PII, and prompt-injection attempts (configured by admins).
- **Administrator controls** — Manage providers, per-user access policies, guardrails, audit logs, gateway performance, and usage-log retention.

## Guides

- [Getting started](./getting-started.md) — Log in and create your first API key.
- [Core features](./user-features.md) — Dashboard, API Keys, Models, and Usage for everyday users.
- [Administrator features](./admin-features.md) — Providers, User Policies, Guardrails, logs, Performance, and Settings.
- [Workflows](./tutorials.md) — End-to-end walkthroughs for common setup tasks.

## At a glance

| Page | Regular User | Administrator |
|---|---|---|
| Dashboard | Own usage stats | Organization-wide stats |
| API Keys | Create / revoke own keys | Create / revoke / restrict any key |
| Models | Browse available models | Browse + manually refresh list |
| Usage | Own request history | All users' request history |
| Providers | — | Add / edit / enable / disable |
| User Policies | — | Set per-user access policies |
| Guardrails | — | Configure, toggle, and test |
| Guardrail Logs | — | View and filter |
| Audit Logs | — | View and filter |
| Performance | — | View gateway metrics |
| Settings | — | Set usage-log retention |

```{toctree}
:hidden:

getting-started
user-features
admin-features
tutorials
```
