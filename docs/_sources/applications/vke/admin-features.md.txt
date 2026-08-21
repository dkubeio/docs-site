# Administrator features

Features available to admins and SRE leads.

## Users

- Manage the roster: add users, assign roles, reset PINs, enable/disable accounts.
- Roles gate which tiles and actions each user sees (see [Getting started](./getting-started.md)).

## Autonomy & safety

- **Autonomy Board** — see which learned fixes are eligible to run and at what tier.
- **T0 master switch** — a single global control (admin-only) to enable or disable
  autonomous action across the cluster.
- **RBAC fencing** — VKE's ServiceAccount is read-only by default. Write is opt-in:
  - `rbac.write: true` grants the fenced verbs (scale, rollout-restart — never delete) cluster-wide.
  - `rbac.writeNamespaces: [...]` grants them in listed namespaces only; everything else stays read-only.

## Training Studio

- Fine-tune domain models on your incident history with cost gating and approval.
- The in-cluster install walks the flow up to the spend gate; the trainer sidecar
  (`trainer.enabled`) runs the fine-tune where a compatible trainer image is available.

## Oversight

- **Analytics / Flywheel** — how VKE's knowledge and success rate improve over time.
- **Audit** — hash-chained event log; every action, approval, and denial is recorded and verifiable.

## Configuration

- **AI endpoint** — point chat and the `k8s-sre` alias at any OpenAI-compatible endpoint
  (the SecureLLM gateway on DKubeX).
- **Cluster mode** — `live` (observe the hosting cluster via the ServiceAccount) or
  `demo` (a bundled synthetic cluster).
