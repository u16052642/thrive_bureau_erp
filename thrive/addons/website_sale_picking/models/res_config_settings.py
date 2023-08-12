# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    picking_site_ids = fields.Many2many(
        'delivery.carrier',
        related='website_id.picking_site_ids',
        readonly=False,
    )
