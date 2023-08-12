# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_note = fields.Text()
