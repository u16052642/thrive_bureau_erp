# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import http

from thrive.addons.website_sale.controllers import main as website_sale_portal
from thrive.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class WebsiteSaleRentingVariantController(WebsiteSaleVariantController):

    @http.route()
    def get_combination_info_website(self, *args, **kwargs):
        res = super(WebsiteSaleRentingVariantController, self).get_combination_info_website(*args, **kwargs)
        res['is_combination_possible'] = res.get('is_combination_possible', True) and res.get('is_recurrence_possible', True)
        return res


class WebsiteSale(website_sale_portal.WebsiteSale):

    def _get_shop_payment_values(self, order, **kwargs):
        """ Override of `website_sale` to specify whether the sales order is a subscription.

        :param recordset order: The sales order being paid, as a `sale.order` record.
        :return: The payment-specific values.
        :rtype: dict
        """
        is_subscription = order.is_subscription or order.subscription_id.is_subscription
        return {
            **super()._get_shop_payment_values(order, **kwargs),
            'is_subscription': is_subscription,
        }
