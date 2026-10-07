# Core features

Day-to-day features for everyday users, grouped by lane.

## Observe

- **Cluster Overview** — nodes, workloads, and health in one view.
- **Nodes / Workloads / Services** — capacity, status, and conditions.
- **Topology** — how workloads and services connect.
- **Cluster Events** — the live event stream.
- **Alerts** — active issues VKE is watching.
- **Telemetry** — health metrics rollup.
- **Discovery / Cloud** — discovered resources and cloud context.

## Converse

- **Chat** — ask questions in natural language; VKE grounds answers in real cluster state
  and can cite the resources it looked at.
- **Playbooks** — reusable, step-by-step runbooks for common situations.
- **Search** — full-text search across events, incidents, and the knowledge base.

## Act

- **Incidents** — track detected issues and their signatures.
- **Approvals** — human-in-the-loop queue: review a proposed fix and approve or deny it.
- **Action Console** — apply **fenced** actions only (scale, rollout-restart); VKE never deletes.
- **Predict** — early signals of likely upcoming issues.

## Learn

- **History** — the append-only, hash-chained event log (the training corpus).
- **Knowledge Base** — shadow-mode fixes VKE has learned, with success/failure counts.
- **Datasets / Models** — training data and the models served to the chat dropdown.

> What you can do in each lane depends on your role — see [Getting started](./getting-started.md).
