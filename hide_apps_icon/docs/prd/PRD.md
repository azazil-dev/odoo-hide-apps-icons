# App Dashboard Visibility

**Technical name:** `hide_apps_icon`
**Version:** 19.0.1.0.0
**Compatibility:** Odoo 19.0 Community and Enterprise
**Price:** Free
**Author:** [Arif N Ramadhan](https://www.niits.id)
**License:** [OPL-1](https://www.odoo.com/documentation/17.0/legal/licenses.html) (Odoo Proprietary License v1.0)

Take full control of what every internal user sees on their Odoo dashboard. With **App Dashboard Visibility**, administrators decide which root applications each security group or each individual user can see, with no programming, no changes to security groups and no risk to existing access rights.

> **Important:** this module only manages **visibility**. It does not grant or revoke access to data models. Odoo groups, ACLs and record rules remain the final authority on access rights. Hiding an app is a user-interface decision, **not a security measure**.

## Features

- Control which root applications appear on the dashboard **per security group** and **per user**.
- User-level settings override group-level settings, so exceptions are easy.
- A **Source** column shows why an app is hidden (a group or a user setting).
- Works on both **Community** (app menu) and **Enterprise** (home menu).
- Hides the app icon, its menu tree and its exclusive actions for the selected user.
- **Check All / Uncheck All** for fast bulk changes.
- **Search Apps** to filter long application lists before toggling.
- Dedicated access right so administrators can delegate visibility management.
- No changes to groups, ACLs or record rules.
- Clean install and uninstall: nothing changes until you hide an app.

## Installation

1. Copy the `hide_apps_icon` folder into your Odoo addons path.
2. Restart the Odoo server.
3. Enable developer mode and go to **Apps → Update Apps List**.
4. Search for **App Dashboard Visibility** and click **Install**.

The module depends only on `base` and `web`.

## How to Use

### Step 1: Grant Access Rights

Navigate to **Settings → Users & Companies → Users**. Select the administrator who should manage visibility, and check the **Manage App Dashboard Visibility** box under their access rights.

### Step 2 (optional): Set Group Defaults

Open **Settings → Users & Companies → Groups**, select a group and go to its **App Dashboard Visibility** tab. Uncheck the apps that every member of this group should not see.

### Step 3: Open the User's Visibility Tab

Open any user and go to the **App Dashboard Visibility** tab. Every root application the user can access is listed there with a **Show on Dashboard** checkbox and a **Source** column.

### Step 4: Hide or Show Apps

- Uncheck an app to hide its icon, menu tree and exclusive actions for that user.
- Use **Check All / Uncheck All** for quick bulk changes.
- Use **Search Apps** to filter a long app list before toggling.
- Use **Reset to Group Defaults** to remove a user's individual settings.

### How Visibility Is Resolved

1. If the user has an individual setting for an app, it wins.
2. Otherwise the app is hidden if at least one of the user's groups hides it.
3. Otherwise the app is visible.

The user sees the change after reloading the browser page.

## Good to Know

- Visibility applies to all of the user's companies.
- Group settings apply to every member of the group, including implied groups.
- Newly installed apps are visible by default.
- Duplicating a user does not copy visibility settings.
- A hidden app can still be reached by direct URL if the user has the access rights. Use Odoo security groups when you need to restrict access.
- The **Settings** app cannot be hidden from Settings administrators.
- Uninstalling the module restores the default Odoo dashboard.

## Technical Information

| Item | Value |
|---|---|
| Technical name | `hide_apps_icon` |
| Depends | `base`, `web` |
| New model | `app.visibility.line` |
| New security group | `hide_apps_icon.group_manage_app_visibility` |
| Extended models | `res.users`, `res.groups`, `ir.ui.menu` |

## Support

For support, bug reports or feature requests, contact **Arif N Ramadhan** at [sqlrif@gmail.com](mailto:sqlrif@gmail.com) or visit [www.niits.id](https://www.niits.id).

## License

This module is licensed under the **Odoo Proprietary License v1.0 (OPL-1)**. See the `LICENSE` file for the full terms. Copyright © Arif N Ramadhan.
