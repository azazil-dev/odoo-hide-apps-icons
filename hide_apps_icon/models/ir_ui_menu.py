# -*- coding: utf-8 -*-
from odoo import models, api

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _get_hidden_app_menu_ids_for_user(self, user):
        """
        Determines the list of root application menu IDs that should be hidden for `user`.
        Resolution rules (from PRD):
        1. If the user has an individual custom setting for an app, it wins.
        2. Otherwise the app is hidden if at least one of the user's groups hides it.
        3. Otherwise the app is visible.
        Rule: The Settings app cannot be hidden from Settings administrators (base.group_system).
        """
        if not user or not user.id:
            return set()

        # Guard: check if app.visibility.line model and table exist in this database
        # (prevents crash before the module is installed or during registry loading)
        if 'app.visibility.line' not in self.env:
            return set()

        self.env.cr.execute("""
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = 'app_visibility_line'
        """)
        if not self.env.cr.fetchone():
            return set()

        settings_menu = self.env.ref('base.menu_administration', raise_if_not_found=False)
        is_settings_admin = user.has_group('base.group_system')

        # 1. User custom lines
        user_lines = self.env['app.visibility.line'].sudo().search([
            ('user_id', '=', user.id),
            ('is_custom', '=', True)
        ])
        user_explicit_hidden = set(user_lines.filtered(lambda l: not l.is_visible).mapped('menu_id.id'))
        user_explicit_shown = set(user_lines.filtered(lambda l: l.is_visible).mapped('menu_id.id'))

        # 2. Group lines
        user_groups = getattr(user, 'group_ids', getattr(user, 'groups_id', self.env['res.groups']))
        group_hidden_lines = self.env['app.visibility.line'].sudo().search([
            ('group_id', 'in', user_groups.ids),
            ('is_visible', '=', False)
        ])
        group_hidden = set(group_hidden_lines.mapped('menu_id.id'))

        # Apps hidden by group, minus those explicitly shown by user setting
        effective_group_hidden = group_hidden - user_explicit_shown

        # Combine
        hidden_ids = user_explicit_hidden | effective_group_hidden

        # Never hide Settings from Settings administrators
        if is_settings_admin and settings_menu and settings_menu.id in hidden_ids:
            hidden_ids.discard(settings_menu.id)

        return hidden_ids

    @api.model
    def get_user_roots(self):
        roots = super().get_user_roots()
        hidden_app_ids = self._get_hidden_app_menu_ids_for_user(self.env.user)
        if hidden_app_ids:
            roots = roots.filtered(lambda m: m.id not in hidden_app_ids)
        return roots

    def _load_menus_blacklist(self):
        res = super()._load_menus_blacklist()
        hidden_app_ids = self._get_hidden_app_menu_ids_for_user(self.env.user)
        if hidden_app_ids:
            res.extend(list(hidden_app_ids))
        return res
