# -*- coding: utf-8 -*-

from thrive import models, fields

from ..models.account_invoice import DESCRIPTION_CREDIT_CODE


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    l10n_co_edi_description_code_credit = fields.Selection(DESCRIPTION_CREDIT_CODE,
                                                           string="Concepto", help="Colombian code for Credit Notes")

    def reverse_moves(self):
        action = super(AccountMoveReversal, self).reverse_moves()
        for refund in self.new_move_ids:
            refund.l10n_co_edi_description_code_credit = self.l10n_co_edi_description_code_credit
        return action