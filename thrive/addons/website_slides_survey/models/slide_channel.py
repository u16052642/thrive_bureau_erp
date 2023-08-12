# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class Channel(models.Model):
    _inherit = 'slide.channel'

    nbr_certification = fields.Integer("Number of Certifications", compute='_compute_slides_statistics', store=True)
