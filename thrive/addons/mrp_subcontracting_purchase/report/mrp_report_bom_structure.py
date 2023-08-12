# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    @api.model
    def _is_buy_route(self, rules, product, bom):
        return super()._is_buy_route(rules, product, bom) and (not bom or bom.type != 'subcontract')
