# Getting started

This guide gets you into SRE and oriented in a few minutes.

## Open SRE

From the DKubeX application catalog, install **SRE**, then open it. SRE is served at
`/vke` behind the platform gateway, so you first pass DKubeX single sign-on, then SRE's
own login screen appears.

## Log in

SRE uses a **PIN-based role login** (no email). Pick your name from the roster and enter
your 4-digit PIN. Each role sees a different set of tiles:

| Role | Focus |
|---|---|
| Admin | Everything, plus user management and the T0 master switch |
| SRE Lead | Approvals, incidents, autonomy tiers |
| Operator | Observe, chat, limited Act |
| ML Engineer | Training Studio, datasets, models |
| Exec | Analytics, flywheel, reports |
| Demo | Read-only: overview, topology, analytics |

> After five failed PIN attempts the account locks; it resets on the next successful login.
> Admins can reset any PIN from the **Users** tile.

## Take the tour

The home screen groups tiles into lanes:

1. **Observe** — start at **Cluster Overview** to see nodes, workloads, and health.
2. **Converse** — open **Chat** and ask a question about your cluster; answers are grounded in live state.
3. **Act** — review **Incidents** and **Approvals** to see proposed remediations.
4. **Learn** — visit **Knowledge Base** and **Training Studio** to see how SRE learns.

## Connect the AI endpoint

SRE talks to any OpenAI-compatible endpoint (on DKubeX this is the SecureLLM gateway).
The model powering chat and the `k8s-sre` alias is configured at install time; an admin
can change it from the settings.
