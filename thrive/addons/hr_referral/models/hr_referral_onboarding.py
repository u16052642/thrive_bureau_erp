# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrReferralOnboarding(models.Model):
    _name = 'hr.referral.onboarding'
    _description = 'Welcome Onboarding in Referral App'
    _order = 'sequence'
    _rec_name = 'text'

    sequence = fields.Integer()
    text = fields.Text(required=True)
    image = fields.Binary(required=True)
    company_id = fields.Many2one('res.company', 'Company')
