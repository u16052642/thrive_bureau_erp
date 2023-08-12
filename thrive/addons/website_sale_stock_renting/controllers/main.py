# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.http import request
from thrive.addons.website_sale_renting.controllers.main import WebsiteSaleRenting
from thrive.addons.website_sale_renting.controllers.product import parse_date


class WebsiteSaleStockRenting(WebsiteSaleRenting):
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        # Override to add rental stock search on /shop
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(attrib_set, options, post, search, website)
        if options.get('from_date') and options.get('to_date'):
            try:
                search_result = search_result._filter_on_available_rental_products(
                    parse_date(options.get('from_date')), parse_date(options.get('to_date')), request.website._get_warehouse_available(),
                )
                product_count = len(search_result)
            except ValueError:
                # Invalid date format
                pass
        return fuzzy_search_term, product_count, search_result
