# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.http import request
from thrive import http

from thrive.addons.website_sale_renting.controllers.product import WebsiteSaleRenting, parse_date

class WebsiteSaleStockRenting(WebsiteSaleRenting):

    @http.route(
        '/rental/product/availabilities', type='json', auth="public", methods=['POST'],
        website=True
    )
    def renting_product_availabilities(self, product_id, min_date, max_date):
        """ Return rental product availabilities.

        Availabilities are the available quantities of a product for a given period. This is
        expressed by an ordered list of dict {'start': ..., 'end': ..., 'available_quantity': ...).

        :rtype: list(dict)
        """
        product_sudo = request.env["product.product"].sudo().browse(product_id).exists()
        result = {'preparation_time': product_sudo.preparation_time}
        if not product_sudo.allow_out_of_stock_order:
            result['renting_availabilities'] = product_sudo._get_availabilities(
                parse_date(min_date), parse_date(max_date),
                request.website._get_warehouse_available(), with_cart=True
            )
        return result
