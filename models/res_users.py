# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    app_visibility_line_ids = fields.One2many(
        'app.visibility.line',
        'user_id',
        string='App Dashboard Visibility',
        copy=False
    )

    def action_refresh_app_visibility(self):
        """Populate or sync visibility lines for apps that the user has access to."""
        self.ensure_one()
        # Find root apps visible to the user under base ACL / groups
        root_menus = self.env['ir.ui.menu'].with_user(self).get_user_roots()
        existing_lines = {line.menu_id.id: line for line in self.app_visibility_line_ids}

        # Check group-level hidden menus for this user
        user_groups = self.groups_id
        group_hidden_menu_ids = set(self.env['app.visibility.line'].search([
            ('group_id', 'in', user_groups.ids),
            ('is_visible', '=', False)
        ]).mapped('menu_id.id'))

        commands = []
        for menu in root_menus:
            if menu.id in existing_lines:
                line = existing_lines[menu.id]
                # If it's not custom, update its default state based on group settings
                if not line.is_custom:
                    expected_visible = menu.id not in group_hidden_menu_ids
                    if line.is_visible != expected_visible:
                        commands.append((1, line.id, {'is_visible': expected_visible}))
            else:
                is_visible = menu.id not in group_hidden_menu_ids
                commands.append((0, 0, {
                    'user_id': self.id,
                    'menu_id': menu.id,
                    'is_custom': False,
                    'is_visible': is_visible,
                }))

        # Remove lines for menus user no longer has access to
        allowed_menu_ids = set(root_menus.ids)
        for menu_id, line in existing_lines.items():
            if menu_id not in allowed_menu_ids:
                commands.append((2, line.id, 0))

        if commands:
            self.with_context(skip_custom_flag=True).write({'app_visibility_line_ids': commands})
        return True

    def action_check_all_apps(self):
        self.action_refresh_app_visibility()
        self.app_visibility_line_ids.write({'is_visible': True, 'is_custom': True})
        return True

    def action_uncheck_all_apps(self):
        self.action_refresh_app_visibility()
        settings_menu = self.env.ref('base.menu_administration', raise_if_not_found=False)
        is_settings_admin = self.has_group('base.group_system')

        for line in self.app_visibility_line_ids:
            if is_settings_admin and settings_menu and line.menu_id.id == settings_menu.id:
                # Do not hide settings app from settings administrator
                line.write({'is_visible': True, 'is_custom': True})
            else:
                line.write({'is_visible': False, 'is_custom': True})
        return True

    def action_reset_to_group_defaults(self):
        """Reset visibility lines to group defaults (clear is_custom)."""
        self.ensure_one()
        user_groups = self.groups_id
        group_hidden_menu_ids = set(self.env['app.visibility.line'].search([
            ('group_id', 'in', user_groups.ids),
            ('is_visible', '=', False)
        ]).mapped('menu_id.id'))

        commands = []
        for line in self.app_visibility_line_ids:
            expected_visible = line.menu_id.id not in group_hidden_menu_ids
            commands.append((1, line.id, {
                'is_custom': False,
                'is_visible': expected_visible,
            }))
        if commands:
            self.with_context(skip_custom_flag=True).write({'app_visibility_line_ids': commands})
        self.action_refresh_app_visibility()
        return True

