## -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Serbia - Accounting Reports',
    'version': '1.0',
    'description': """
        Accounting reports for Serbia
    """,
    "author": "Mthrivelar, Thrive Bureau ERP",
    'category': 'Accounting/Localizations/Reporting',
    'depends': [
        'l10n_rs',
        'account_reports',
    ],
    'data': [
        'data/profit_and_loss.xml',
        'data/balance_sheet.xml',
    ],
    'auto_install': True,
    'installable': True,
    'license': 'OEEL-1',
}
