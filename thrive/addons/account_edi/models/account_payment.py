# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_process_edi_web_services(self):
        return self.move_id.action_process_edi_web_services()

    def action_retry_edi_documents_error(self):
        self.ensure_one()
        return self.move_id.action_retry_edi_documents_error()
