# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': "Sale Accounting",
    'version': "1.0",
    'category': "Sales/Sales",
    'summary': "Bridge between Sale and Accounting",
    'description': """
Notify that a matching sale order exists in the reconciliation widget.
    """,
    'depends': ['sale', 'account_accountant'],
    'data': [
        'views/bank_rec_widget_views.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
