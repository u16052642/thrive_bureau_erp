# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    followup_line_id = fields.Many2one('account_followup.followup.line', 'Follow-up Level', copy=False)
    last_followup_date = fields.Date('Latest Follow-up', index=True, copy=False)
    next_action_date = fields.Date('Next Action Date',
                                   help="Date where the next action should be taken for a receivable item. Usually, "
                                        "automatically set when sending reminders through the customer statement.")
    invoice_date = fields.Date(related='move_id.invoice_date')
    invoice_origin = fields.Char(related='move_id.invoice_origin')
