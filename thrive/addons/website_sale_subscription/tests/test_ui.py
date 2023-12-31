# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import HttpCase, tagged
from .common import TestWebsiteSaleSubscriptionCommon

@tagged('-at_install', 'post_install')
class TestUi(HttpCase, TestWebsiteSaleSubscriptionCommon):

    def test_website_sale_subscription_ui(self):
        self.start_tour("/web", 'shop_buy_subscription_product', login='admin')
