# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_product_updatable(self):
        temporal_lines = self.filtered('temporal_type')
        super(SaleOrderLine, self - temporal_lines)._compute_product_updatable()
        temporal_lines.product_updatable = True
