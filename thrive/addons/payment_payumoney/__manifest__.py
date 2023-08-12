# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: PayUmoney',
    'version': '2.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "This module is deprecated.",
    'depends': ['payment'],
    'data': [
        'views/payment_payumoney_templates.xml',
        'views/payment_provider_views.xml',

        'data/payment_provider_data.xml',
    ],
    'application': False,
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
