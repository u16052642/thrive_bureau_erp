# -*- coding: utf-8 -*-
from thrive import api, models, fields, _
from thrive.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_government_document(self):
        linked_edi_documents = self.env['account.edi.document'].search([('attachment_id', 'in', self.ids)])
        linked_edi_formats_ws = linked_edi_documents.edi_format_id.filtered(lambda edi_format: edi_format._needs_web_services())
        if linked_edi_formats_ws:
            raise UserError(_("You can't unlink an attachment being an EDI document sent to the government."))
