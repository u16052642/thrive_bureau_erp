# -*- encoding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Consolidation Demo Data',
    'icon': '/l10n_be/static/description/icon.png',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 50,
    'summary': 'Account Consolidation Demo Data using a Belgium and a US company',
    'depends': ['account_consolidation', 'l10n_be', 'l10n_generic_coa'],
    'description': """
Account Consolidation Demo Data
==================================
""",
    'demo': [
        'data/consolidation_config.xml',
        'data/liaison_accounts.xml',
        'data/invoices.xml',
        'data/liaison_invoices.xml',
        'data/consolidation_generate.xml',
        'data/consolidation_of_consolidation.xml'
    ],
    'auto_install': True,
    'license': 'OEEL-1',
}
