# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Helpdesk Account',
    'category': 'Services/Helpdesk',
    'summary': 'Project, Tasks, Account',
    'depends': ['helpdesk_sale', 'account'],
    'description': """
Create Credit Notes from Helpdesk tickets
    """,
    'data': [
        'wizard/account_move_reversal_views.xml',
        'views/helpdesk_views.xml',
    ],
    'demo': [
       'data/helpdesk_account_demo.xml'
    ],
    'license': 'OEEL-1',
}
