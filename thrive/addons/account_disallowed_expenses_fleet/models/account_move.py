# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, api
from thrive.tools import frozendict


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('vehicle_id')
    def _compute_tax_key(self):
        super()._compute_tax_key()
        for line in self:
            if line.vehicle_id:
                line.tax_key = frozendict(**line.tax_key, vehicle_id=line.vehicle_id.id)

    @api.depends('vehicle_id')
    def _compute_all_tax(self):
        super()._compute_all_tax()
        for line in self:
            if line.vehicle_id:
                for key in list(line.compute_all_tax.keys()):
                    new_key = frozendict(**key, vehicle_id=line.vehicle_id.id)
                    line.compute_all_tax[new_key] = line.compute_all_tax.pop(key)

    @api.depends('account_id.disallowed_expenses_category_id')
    def _compute_need_vehicle(self):
        for record in self:
            record.need_vehicle = record.account_id.disallowed_expenses_category_id.sudo().car_category and record.move_id.move_type == 'in_invoice'
