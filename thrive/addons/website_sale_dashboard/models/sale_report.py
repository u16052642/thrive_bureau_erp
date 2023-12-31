# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class SaleReport(models.Model):
    _inherit = 'sale.report'

    is_abandoned_cart = fields.Boolean(string="Abandoned Cart", readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['is_abandoned_cart'] = """
            s.date_order <= (timezone('utc', now()) - ((COALESCE(w.cart_abandoned_delay, '1.0') || ' hour')::INTERVAL))
            AND s.website_id IS NOT NULL
            AND s.state = 'draft'
            AND s.partner_id != %s""" % self.env.ref('base.public_partner').id
        return res

    def _from_sale(self):
        res = super()._from_sale()
        res += """
            LEFT JOIN website w ON w.id = s.website_id"""
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            w.cart_abandoned_delay"""
        return res
