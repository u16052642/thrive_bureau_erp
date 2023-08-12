# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, models
from thrive.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def _get_bank_statements_available_import_formats(self):
        rslt = super()._get_bank_statements_available_import_formats()
        rslt.append('CSV')
        return rslt

    def _check_csv(self, filename):
        return filename and filename.lower().strip().endswith('.csv')

    def _import_bank_statement(self, attachments):
        # In case of CSV files, only one file can be imported at a time.
        if len(attachments) > 1:
            csv = [bool(self._check_csv(att.name)) for att in attachments]
            if True in csv and False in csv:
                raise UserError(_('Mixing CSV files with other file types is not allowed.'))
            if csv.count(True) > 1:
                raise UserError(_('Only one CSV file can be selected.'))
            return super()._import_bank_statement(attachments)

        if not self._check_csv(attachments.name):
            return super()._import_bank_statement(attachments)
        ctx = dict(self.env.context)
        import_wizard = self.env['base_import.import'].create({
            'res_model': 'account.bank.statement.line',
            'file': attachments.raw,
            'file_name': attachments.name,
            'file_type': attachments.mimetype,
        })
        ctx['wizard_id'] = import_wizard.id
        ctx['default_journal_id'] = self.id
        return {
            'type': 'ir.actions.client',
            'tag': 'import_bank_stmt',
            'params': {
                'model': 'account.bank.statement.line',
                'context': ctx,
                'filename': 'bank_statement_import.csv',
            }
        }