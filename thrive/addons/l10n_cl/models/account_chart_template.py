# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models
from thrive.http import request


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _load(self, company):
        """ Set tax calculation rounding method required in Chilean localization"""
        res = super()._load(company)
        if company.account_fiscal_country_id.code == 'CL':
            company.write({'tax_calculation_rounding_method': 'round_globally'})
        return res
