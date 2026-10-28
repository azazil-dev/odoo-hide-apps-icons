# -*- coding: utf-8 -*-
{
    'name': "App Dashboard Visibility",
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'summary': "Control root applications dashboard visibility per group and per user",
    'description': """
App Dashboard Visibility
========================
Take full control of what every internal user sees on their Odoo dashboard.
With App Dashboard Visibility, administrators decide which root applications each security group
or each individual user can see, with no programming, no changes to security groups and no risk
to existing access rights.

Features:
- Control which root applications appear on the dashboard per security group and per user.
- User-level settings override group-level settings, so exceptions are easy.
- A Source column shows why an app is hidden (a group or a user setting).
- Works on both Community (app menu) and Enterprise (home menu).
- Hides the app icon, its menu tree and its exclusive actions for the selected user.
- Check All / Uncheck All for fast bulk changes.
- Dedicated access right (Manage App Dashboard Visibility) so administrators can delegate visibility management.
- No changes to groups, ACLs or record rules.
- Clean install and uninstall: nothing changes until you hide an app.
    """,
    'author': "Arif N Ramadhan",
    'website': "https://www.niits.id",
    'license': 'OPL-1',
    'price': 0.00,
    'currency': 'EUR',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/security_data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
