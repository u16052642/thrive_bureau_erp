# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Poland - Accounting Reports',
    'version': '1.0',
    'description': """
        Accounting reports for Poland
    """,
    'category': 'Accounting/Localizations/Reporting',
    'depends': [
        'l10n_pl',
        'account_reports',
    ],
    'data': [
        'data/profit_loss_small.xml',
        'data/profit_loss_micro.xml',
        'data/balance_sheet_small.xml',
        'data/balance_sheet_micro.xml',
    ],
    'auto_install': True,
    'installable': True,
    'website': 'https://www.thrivebureau.com/app/accounting',
    'license': 'OEEL-1',
}
