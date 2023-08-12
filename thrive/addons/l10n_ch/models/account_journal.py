# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields, api

from thrive.exceptions import ValidationError

from thrive.addons.base_iban.models.res_partner_bank import validate_iban
from thrive.addons.base.models.res_bank import sanitize_account_number


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    invoice_reference_model = fields.Selection(selection_add=[
        ('ch', 'Switzerland')
    ], ondelete={'ch': lambda recs: recs.write({'invoice_reference_model': 'thrive'})})
