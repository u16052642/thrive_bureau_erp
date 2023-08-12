# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': 'EDI for Mexico (Advanced Features)',
    'icon': '/l10n_mx/static/description/icon.png',
    'version': '0.1',
    'category': 'Hidden',
    'depends': [
        'l10n_mx_edi',
        'base_address_extended',
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/3.3/cfdi.xml',
        'data/product_data.xml',
        'data/uom_uom_data.xml',

        'views/l10n_mx_edi_tariff_fraction_view.xml',
        'views/account_journal_view.xml',
        'views/account_move_view.xml',
        'views/product_template_view.xml',
        'views/uom_uom_view.xml',
        'views/res_company_view.xml',
        'views/res_config_settings_view.xml',
        'views/res_partner_views.xml',
        'views/report_invoice.xml',

        'data/country.xml',
    ],
    'demo': [
        'demo/demo_cfdi.xml',
    ],
    'installable': True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'OEEL-1',
}