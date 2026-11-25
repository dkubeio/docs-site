# User Management

Manage user accounts from the admin console under **Users**. The Users page lists every account with
its **Full Name**, **Email**, and **Role**.

DKubeX supports two sign-in modes, which changes how accounts are created:

- **Local password** — administrators create accounts by hand (below).
- **OAuth (GitHub / SSO)** — accounts are created automatically the first time a user signs in. In this
  mode **Add User** is disabled ("Users are managed via OAuth provider").

## Add a user

*(Local password mode.)*

1. Open the admin console → **Users**.
2. Click **Add User**.
3. Fill in the form:
   | Field | Notes |
   |---|---|
   | **Email** *(required)* | The user's sign-in identity. Cannot be changed later. |
   | **Full Name** | Optional. |
   | **Set Password** *(required)* | Use the eye icon to reveal it. |
   | **Confirm Password** *(required)* | Must match. |
   | **Is superuser?** | Check to grant admin-console access. |
4. Click **Save**. The user appears in the table.

## Edit a user

1. On the **Users** page, open the **⋮** menu on the user's row → **Edit User**.
2. Change any of:
   - **Full Name**
   - **Set Password** / **Confirm Password** — resets the user's password.
   - **Is superuser?** — promotes or demotes admin access.
3. Click **Save**.

The **Email** field is read-only — a user's email is their identity and cannot be changed after the
account exists.

## Assign application roles to a user

Give a user a role in the platform tools, workspace apps, and coding agents:

1. On the **Users** page, open the **⋮** menu on the user's row → **Manage Roles**.
2. For each application in the list, set the access level from the dropdown:
   - **No Access**
   - **User**
   - **Admin**
3. Save.

:::{note}
To grant access to an **installed catalog application** (ModelStudio, SecureLLM, RAGFlow, and so on),
assign the user from the application instead — see
[Application Management → Manage users and roles](application-management.md#manage-users-and-roles-for-an-application).
:::

## Delete a user

1. On the **Users** page, open the **⋮** menu on the user's row → **Delete User**.
2. Confirm.

You cannot delete your own account, so the option does not appear on your own row.

## Roles and permissions

DKubeX has two kinds of role:

- A **platform role**: every account is either a superuser (administrator) or a regular user. The
  **Is superuser?** checkbox sets it.
- An **application role**: for each application a user is assigned to, the role is **User** or
  **Admin**.

### Platform roles

| Action | Superuser | Regular user |
|---|---|---|
| Open the admin console (**Dashboard, Applications, Workspaces, Users, Licenses, Config, Platform**) | Yes | No |
| Install an application from the App Store | Yes | Yes. When the install is ready, the application is assigned to the user who installed it, with the **Admin** role. |
| Edit an application's Helm values when installing it | Yes | No |
| Cancel an install that is still in progress | Yes, any install | Only an install they started |
| Upgrade, reconfigure (**Edit Values & Update**) or uninstall an installed application | Yes | No |
| View an application's install logs | Yes | No |
| Assign users to an application and set their roles | Yes | No |
| Request access to an application | Not needed (superusers can open every application) | Yes (see [Access Requests](access-requests.md)) |
| Approve or dismiss access requests | Yes | No |
| Add, edit and delete users | Yes | No |
| Upload, view and delete licenses | Yes | No |
| Change the platform configuration and credentials (**Config**) | Yes | No |
| Upgrade the platform (**Platform**) | Yes | No |
| Manage Helm repositories | Yes | No |
| Manage all users' workspaces | Yes | No |
| Install or remove their own workspace | Yes | Yes |
| Open a workspace | Any user's workspace | Only their own |

### Application roles

- A user can open an application only when they are assigned to it. Without an assignment, DKubeX
  denies access, and the user can request it (see [Access Requests](access-requests.md)).
- DKubeX passes the user's application role to the application in the `X-Auth-Request-Role` header,
  as `user` or `admin`. If no role is set, the value is `user`.
- Superusers can open every application and are always sent as `admin`.
- DKubeX does not decide what **Admin** allows inside an application. Each application uses the role
  in its own way.
