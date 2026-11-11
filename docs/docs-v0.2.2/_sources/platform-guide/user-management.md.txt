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
To grant access to an **installed catalog application** (Model Studio, SecureLLM, RAGFlow, and so on),
assign the user from the application instead — see
[Application Management → Manage users and roles](application-management.md#manage-users-and-roles-for-an-application).
:::

## Delete a user

1. On the **Users** page, open the **⋮** menu on the user's row → **Delete User**.
2. Confirm.

You cannot delete your own account, so the option does not appear on your own row.
