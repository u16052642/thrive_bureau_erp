# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class DepartureReason(models.Model):
    _inherit = "hr.departure.reason"

    reason_code = fields.Integer()

    def _get_default_departure_reasons(self):
        return {
            **super()._get_default_departure_reasons(),
            'freelance': 350,
        }
