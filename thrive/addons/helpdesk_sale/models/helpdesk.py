# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, Command, fields, models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    @api.model_create_multi
    def create(self, vals_list):
        teams = super().create(vals_list)
        teams.sudo()._check_helpdesk_sale_timesheet_group()
        return teams

    def write(self, vals):
        result = super().write(vals)
        if 'use_helpdesk_sale_timesheet' in vals:
            self.sudo()._check_helpdesk_sale_timesheet_group()
        return result

    def _check_sale_timesheet_feature_enabled(self):
        """ Check if the Time Billing feature is enabled

            Check if the user can see at least one helpdesk team with `use_helpdesk_sale_timesheet=True`

            :return True if the feature is enabled otherwise False.
        """
        return self.env['helpdesk.team'].search([('use_helpdesk_sale_timesheet', '=', True)], limit=1)

    def _check_helpdesk_sale_timesheet_group(self):
        use_sale_timesheet_group = self.env.ref('helpdesk_sale.group_use_helpdesk_sale_timesheet')
        sale_teams = self.filtered('use_helpdesk_sale_timesheet')
        user_has_use_sale_timesheet_group = self.user_has_groups('helpdesk_sale.group_use_helpdesk_sale_timesheet')

        if sale_teams and not user_has_use_sale_timesheet_group:
            self._get_helpdesk_user_group()\
                .write({'implied_ids': [Command.link(use_sale_timesheet_group.id)]})
        elif not sale_teams and user_has_use_sale_timesheet_group and not self._check_sale_timesheet_feature_enabled():
            self._get_helpdesk_user_group()\
                .write({'implied_ids': [Command.unlink(use_sale_timesheet_group.id)]})
            use_sale_timesheet_group.write({'users': [Command.clear()]})


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sale_order_id = fields.Many2one('sale.order', string='Ref. Sales Order',
        domain="""[
            '|', (not commercial_partner_id, '=', 1), ('partner_id', 'child_of', commercial_partner_id or []),
            ('company_id', '=', company_id)]""",
        groups="sales_team.group_sale_salesman,account.group_account_invoice")

    def copy(self, default=None):
        if not self.env.user.has_group('sales_team.group_sale_salesman') and not self.env.user.has_group('account.group_account_invoice'):
            if default is None:
                default = {'sale_order_id': False}
            else:
                default.update({'sale_order_id': False})
        return super(HelpdeskTicket, self).copy(default=default)
