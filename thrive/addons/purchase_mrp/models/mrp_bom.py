# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models, _
from thrive.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def _check_bom_lines(self):
        res = super()._check_bom_lines()
        for bom in self:
            if all(not bl.cost_share for bl in bom.bom_lines):
                continue
            if any(bl.cost_share < 0 for bl in bom.bom_lines):
                raise UserError(_("Components cost share have to be positive or equals to zero."))
            if sum(bom.bom_lines.mapped('cost_share')) != 100:
                raise UserError(_("The total cost share for a BoM's component have to be 100"))
        return res


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    cost_share = fields.Float(
        "Cost Share (%)", digits=(5, 2),  # decimal = 2 is important for rounding calculations!!
        help="The percentage of the component repartition cost when purchasing a kit."
             "The total of all components' cost have to be equal to 100.")

    def _get_cost_share(self):
        self.ensure_one()
        if self.cost_share:
            return fields.Float.round(self.cost_share / 100, 2)
        bom = self.bom_id
        bom_lines_without_cost_share = bom.bom_line_ids.filtered(lambda bl: not bl.cost_share)
        return fields.Float.round(1 / len(bom_lines_without_cost_share), 2)
