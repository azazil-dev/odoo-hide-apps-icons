# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command

class ResGroups(models.Model):
    _inherit = 'res.groups'

    app_visibility_line_ids = fields.One2many(
        'app.visibility.line',
        'group_id',
        string='App Dashboard Visibility',
        copy=False
    )

    def action_load_apps_visibility(self):
        """Populate root apps into app_visibility_line_ids if not already present."""
        self.ensure_one()
        root_menus = self.env['ir.ui.menu'].search([('parent_id', '=', False)])
        existing_menu_ids = self.app_visibility_line_ids.mapped('menu_id.id')
        new_lines = []
        for menu in root_menus:
            if menu.id not in existing_menu_ids:
                new_lines.append(Command.create({
                    'group_id': self.id,
                    'menu_id': menu.id,
                    'is_visible': True,
                }))
        if new_lines:
            self.write({'app_visibility_line_ids': new_lines})
        return True

    def action_check_all_apps(self):
        self.action_load_apps_visibility()
        self.app_visibility_line_ids.write({'is_visible': True})
        return True

    def action_uncheck_all_apps(self):
        self.action_load_apps_visibility()
        self.app_visibility_line_ids.write({'is_visible': False})
        return True

