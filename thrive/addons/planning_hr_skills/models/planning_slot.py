# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models

class PlanningSlot(models.Model):
    _inherit = 'planning.slot'

    employee_skill_ids = fields.One2many(related='employee_id.employee_skill_ids', string='Skills')
