# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': "Analytic Accounting Enterprise",
    'version': '0.1',
    'website': "https://www.ThriveERP.com/app/accounting",
    'category': 'Accounting/Accounting',
    'depends': ['web_grid', 'analytic', 'account'],
    'description': """
Module for defining analytic accounting object.
===============================================

In Thrive, analytic accounts are linked to general accounts but are treated
totally independently. So, you can enter various different analytic operations
that have no counterpart in the general financial accounts.
    """,
    'data': [
        'views/account_analytic_view.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
