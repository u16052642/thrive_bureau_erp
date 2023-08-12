# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive.addons.account.models.chart_template import update_taxes_from_templates


def migrate(cr, version):
    update_taxes_from_templates(cr, 'l10n_lu.lu_2011_chart_1')
