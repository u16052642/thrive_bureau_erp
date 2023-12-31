# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sla_id = fields.Many2one(
        "helpdesk.sla", string="SLA Policy",
        company_dependent=True,
        domain="[('company_id', '=', current_company_id)]",
        help="SLA Policy that will automatically apply to the tickets linked to a sales order item containing this service.")
