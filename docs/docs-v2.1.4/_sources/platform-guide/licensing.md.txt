# Licensing

DKubeX applications are gated by seat-based licenses. Manage them from the admin console under
**Licenses**, which has two tabs — **Licenses** and **License Requests**.

Each application runs on a **30-day trial** when first registered. After the trial, a valid license
with available seats is required for users to keep access. A license is issued for **one cluster** and
grants a number of **seats** per application (one seat per user, per application).

## Get your Cluster ID

A license is bound to your cluster, so DKube needs your Cluster ID to issue one.

1. Open the admin console → **Licenses**.
2. In the **Cluster ID** card, click the copy icon.
3. Share the Cluster ID with DKube when requesting a license.

## Add (upload) a license

1. When you receive the license file (JSON) from DKube, open **Licenses**.
2. Click **Upload License**.
3. Select the license file.

The license appears in the table with its ID, company, covered applications, issued date, expiry, and
status.

## View license details and seats

1. On the **Licenses** tab, open a license.
2. The detail view shows, per application, the **seats used / seats max** and the list of seat holders.
3. Remove a user's seat from here if you need to free a seat.

Licenses aggregate: if more than one active license covers an application, its total seats are the sum
across those licenses.

## Handle license requests

When a user is blocked (trial expired, no seat available, or license expired), they can raise a request.

1. Open **Licenses** → the **License Requests** tab.
2. Review the request and **resolve** it.

Resolving a request acknowledges it; grant the user access or free a seat separately as needed.

## Renew or remove a license

- **Renew** — upload a new license file (**Upload License**). Existing licenses keep running until their
  own expiry; the new one adds its seats and validity.
- **Remove** — an expired license can be deleted from the **Licenses** tab.

## License states

| Level | States |
|---|---|
| Per license | **active**, **expiring soon** (≤ 30 days left), **expired** |
| Per application | **trial**, **licensed**, **expired**, **none** |
