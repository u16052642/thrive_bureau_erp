# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive import http

from thrive.addons.website_sale.controllers.main import WebsiteSale
from thrive.addons.website_sale_renting.controllers.product import parse_date


class WebsiteSaleRenting(WebsiteSale):

    @http.route()
    def cart_options_update_json(self, *args, start_date=None, end_date=None, **kwargs):
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        return super().cart_options_update_json(
            *args, start_date=start_date, end_date=end_date, **kwargs
        )
