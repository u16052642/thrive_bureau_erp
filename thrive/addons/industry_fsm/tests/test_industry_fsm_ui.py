# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-

import thrive.tests


@thrive.tests.tagged('post_install', '-at_install')
class TestUi(thrive.tests.HttpCase):
    def test_ui(self):
        self.env['res.partner'].create({'name': 'Leroy Philippe', 'email': 'leroy.philou@example.com'})
        self.start_tour("/web", 'industry_fsm_tour', login="admin")
