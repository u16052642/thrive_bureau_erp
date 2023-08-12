#-*- coding:utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def unlink(self):
        journal = self.env.ref('hr_payroll_account.hr_payroll_account_journal')
        return super(AccountJournal, self.filtered(lambda j: j != journal)).unlink()
