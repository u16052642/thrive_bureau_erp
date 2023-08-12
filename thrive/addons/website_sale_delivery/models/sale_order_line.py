# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _show_in_cart(self):
        # Exclude delivery line from showing up in the cart
        return not self.is_delivery and super()._show_in_cart()
