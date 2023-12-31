# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    quality_check_ids = fields.One2many('quality.check', 'move_line_id', string='Check')

    def _without_quality_checks(self):
        self.ensure_one()
        return not self.quality_check_ids
