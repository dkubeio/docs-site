# Workflows

End-to-end walkthroughs for common tasks.

## Investigate an incident

1. Open **Incidents** and select an active one.
2. Read the grounded summary and the signature VKE assigned.
3. Ask follow-up questions in **Chat** — answers cite the live resources involved.
4. If VKE proposes a fix, it appears in **Approvals**.

## Approve and apply a fenced fix

1. Go to **Approvals** and open the pending proposal.
2. Review the fenced action (scale or rollout-restart — never delete) and the target.
3. **Approve** to apply it via the Action Console, or **Deny**.
4. The outcome is recorded in **History** and updates the fix's stats in the **Knowledge Base**.

## Ground a question in cluster state

1. Open **Chat**.
2. Ask, e.g., "why is the payments deployment not ready?"
3. VKE inspects the relevant pods/events and answers with citations.

## Train a domain model

1. Open **Training Studio** and pick a base model and dataset.
2. Review the estimated cost; the flow stops at the **spend gate**.
3. With the trainer enabled and approved, the fine-tune runs; the resulting model is
   imported and appears in the chat model dropdown.

## Grant scoped write access

1. As an admin, decide the blast radius: cluster-wide vs specific namespaces.
2. Set `rbac.write` or `rbac.writeNamespaces` at install/upgrade time.
3. Toggle the **T0 master switch** to enable autonomous action when ready.
