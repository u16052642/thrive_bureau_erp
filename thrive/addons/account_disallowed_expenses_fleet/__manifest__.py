# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': 'Disallowed Expenses on Fleets',
    'category': 'Accounting/Accounting',
    'summary': 'Manage disallowed expenses with fleets',
    'version': '1.0',
    'depends': ['account_fleet', 'account_disallowed_expenses'],
    'data': [
        'security/ir.model.access.csv',
        'data/account_disallowed_expenses_fleet_report.xml',
        'views/account_disallowed_expenses_category_views.xml',
        'views/fleet_vehicle_views.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
