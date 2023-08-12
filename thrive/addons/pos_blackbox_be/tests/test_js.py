# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive.tests


@thrive.tests.tagged('-at_install', 'post_install')
class WebSuite(thrive.tests.HttpCase):
    def test_01_js(self):
        self.browser_js('/web/tests?module=pos_blackbox_be.Order',"","", login='admin')
