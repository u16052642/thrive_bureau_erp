# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    disallowed_expenses_category_id = fields.Many2one('account.disallowed.expenses.category', string='Disallowed Expenses Category', domain="['|', ('company_id', '=', company_id), ('company_id', '=', False)]")

    @api.onchange('internal_group')
    def _onchange_internal_group(self):
        if self.internal_group not in ('income', 'expense'):
            self.disallowed_expenses_category_id = None
