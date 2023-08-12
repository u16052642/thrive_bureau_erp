# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import math
from datetime import date

from dateutil.relativedelta import relativedelta
from thrive import models


class HRPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _get_base_local_dict(self):
        res = super()._get_base_local_dict()
        res.update({
            "relativedelta": relativedelta,
            "date": date,
            "ceil": math.ceil
        })
        return res
