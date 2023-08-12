# -*- coding:utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    l10n_lu_atn_transport = fields.Monetary("BIK Transport")
