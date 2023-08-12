# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, fields, models
from thrive.tools.translate import html_translate


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    website_description = fields.Html(
        string="Website Description",
        compute='_compute_website_description',
        store=True, readonly=False, precompute=True,
        sanitize=False, translate=html_translate, sanitize_form=False)

    @api.depends('product_id')
    def _compute_website_description(self):
        for line in self:
            if not line.product_id:
                continue
            line.website_description = line.product_id.with_context(
                lang=line.order_partner_id.lang
            ).quotation_description
