# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    first_contract_date = fields.Date(readonly=True, groups="base.group_user")
