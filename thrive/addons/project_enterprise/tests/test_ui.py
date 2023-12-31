# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import HttpCase, tagged

@tagged('-at_install', 'post_install')
class TestUi(HttpCase):
    def test_01_ui(self):
        self.start_tour("/", 'project_enterprise_tour', login='admin')
