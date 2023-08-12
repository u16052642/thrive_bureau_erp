# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class SriPayment(models.Model):

    _name = "l10n_ec.sri.payment"
    _description = "SRI Payment Method"

    name = fields.Char("Name")
    code = fields.Char("Code")
