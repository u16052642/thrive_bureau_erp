# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models


class TaskCustomReport(models.AbstractModel):
    _inherit = 'report.industry_fsm.worksheet_custom'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = super()._get_report_values(docids, data)
        worksheet_map = {}
        for task in data.get('docs'):
            if task.worksheet_template_id:
                x_model = task.worksheet_template_id.model_id.model
                worksheet = self.env[x_model].search([('x_project_task_id', '=', task.id)], limit=1, order="create_date DESC")  # take the last one
                worksheet_map[task.id] = worksheet

        data.update({'worksheet_map': worksheet_map})
        return data
