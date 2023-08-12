# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class ProposeChange(models.TransientModel):
    _inherit = 'propose.change'

    def _workorder_name(self):
        if self.workorder_id.employee_id:
            return self.workorder_id.employee_id.name
        return super()._workorder_name()
