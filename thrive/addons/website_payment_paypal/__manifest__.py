# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website - Payment Paypal',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 365,
    'summary': 'Website - Payment Paypal',
    'depends': ['website_payment', 'payment_paypal'],
    'data': [
        'views/res_config_settings_views.xml'
    ],
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
