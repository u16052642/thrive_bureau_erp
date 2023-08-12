# -*- coding: utf-8 -*-

from thrive.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleTaxcloudDelivery(WebsiteSale):

    def _update_website_sale_delivery_return(self, order, **post):
        if order and order.fiscal_position_id.is_taxcloud:
            order.validate_taxes_on_sales_order()
        return super(WebsiteSaleTaxcloudDelivery, self)._update_website_sale_delivery_return(order, **post)
