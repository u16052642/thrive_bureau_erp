# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class UtmCampaign(models.Model):
    _inherit = 'utm.campaign'

    ab_testing_winner_selection = fields.Selection(selection_add=[('crm_lead_count', 'Leads')])