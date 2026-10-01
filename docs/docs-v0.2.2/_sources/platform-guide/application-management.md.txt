# Application Management

Install and manage applications from the admin console under **Applications**. Applications are
installed as declarative Kubernetes resources (an `Application` custom resource that the platform
reconciles into a Helm release), so you never run Helm by hand.

The **Applications** page has three tabs — **Applications** (installed), **Browse Catalog**, and
**Access Requests** — plus a **Manage Repositories** button.

## View installed applications

On the **Applications** tab, each installed application shows its name, **version**, and **CRD** name,
with an **Actions** menu. The status filters on the left group applications by state:

| Filter | Meaning |
|---|---|
| **Installed** | Running applications. |
| **Failed** | Installations that did not complete. |
| **Trial / Licensed / Expired** | Licensing state (see [Licensing](licensing.md)). |

Search installed applications by name with the search box.

## Install an application

1. Open the **Browse Catalog** tab.
2. Narrow the list if needed:
   - **Use Case** filter (AI/ML, Developer Tools, Machine Learning, Monitoring).
   - **Upgrade available** — show only applications with a newer version.
   - **Sort by** — Default, Name (A–Z / Z–A), or Category.
3. On the application's card, click **Install**.
4. Track progress on the **Applications** tab — the status moves through **Installing → Starting →
   Ready**.

If an install fails, the application appears under the **Failed** filter, where you can review the
reason and retry.

(manage-users-and-roles-for-an-application)=
## Manage users and roles for an application

1. On the **Applications** tab, open **Actions** on the installed application → **Manage Users & Roles**.
2. Assign users and set each user's role (**User** or **Admin**).
3. Save.

The assigned users can open the application through single sign-on on their next sign-in.

## Upgrade or reconfigure an application

1. On the **Applications** tab, open **Actions** on the installed application → **Edit Values & Update**.
2. Change the version and/or the Helm values.
3. Apply the update. The application updates in place and stays available.

## Uninstall an application

1. On the **Applications** tab, open **Actions** on the installed application → **Uninstall**.
2. Confirm.

The application is removed and returns to the catalog with an **Install** button.

## Manage repositories

The catalog aggregates applications from the registered Helm repositories.

1. On the **Applications** page, click **Manage Repositories**.
2. Add or remove Helm repositories.

Newly added repositories' applications appear in **Browse Catalog** (the catalog refreshes
periodically; use the refresh control to update immediately).
