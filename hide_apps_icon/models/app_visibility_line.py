# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AppVisibilityLine(models.Model):
    _name = 'app.visibility.line'
    _description = 'App Dashboard Visibility Line'
    _order = 'sequence, name'

    user_id = fields.Many2one('res.users', string='User', ondelete='cascade', index=True)
    group_id = fields.Many2one('res.groups', string='Group', ondelete='cascade', index=True)
    menu_id = fields.Many2one('ir.ui.menu', string='Application', required=True, ondelete='cascade', index=True)
    name = fields.Char(related='menu_id.name', string='App Name', store=True, readonly=True)
    sequence = fields.Integer(related='menu_id.sequence', string='Sequence', store=True, readonly=True)

    # For user line:
    # is_custom = True means user explicitly set Show/Hide
    # is_custom = False means user has no explicit override, line is computed from group defaults or visible by default
    is_custom = fields.Boolean(string='Is Custom Setting', default=False)
    is_visible = fields.Boolean(string='Show on Dashboard', default=True)
    source = fields.Char(string='Source', compute='_compute_source', readonly=True)

    @api.depends('is_custom', 'is_visible', 'user_id', 'group_id', 'menu_id')
    def _compute_source(self):
        for line in self:
            if line.group_id:
                line.source = _('Group Setting')
            elif line.user_id:
                if line.is_custom:
                    line.source = _('User Setting')
                else:
                    # Check if any group of this user hides it
                    user_groups = line.user_id.groups_id
                    group_lines = self.search([
                        ('group_id', 'in', user_groups.ids),
                        ('menu_id', '=', line.menu_id.id),
                        ('is_visible', '=', False)
                    ])
                    if group_lines:
                        group_names = ", ".join(group_lines.mapped('group_id.name'))
                        line.source = _('Group: %s') % group_names
                    else:
                        line.source = _('Default')
            else:
                line.source = _('Default')

    def write(self, vals):
        if 'is_visible' in vals and not self.env.context.get('skip_custom_flag'):
            for line in self:
                if line.user_id and not line.is_custom:
                    vals['is_custom'] = True
        res = super().write(vals)
        self.env.registry.clear_cache()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self.env.registry.clear_cache()
        return records

    def unlink(self):
        res = super().unlink()
        self.env.registry.clear_cache()
        return res

