# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class AnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = ['account.analytic.line']

    def _should_not_display_timer(self):
        self.ensure_one()
        return super()._should_not_display_timer() or self.task_id.is_timeoff_task
