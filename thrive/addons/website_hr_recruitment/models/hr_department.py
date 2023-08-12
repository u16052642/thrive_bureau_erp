# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class Department(models.Model):
    _inherit = 'hr.department'

    def name_get(self):
        # Get department name using superuser, because model is not accessible
        # for portal users
        self_sudo = self.sudo()
        return super(Department, self_sudo).name_get()
