# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Invoice Extract',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Extract data from invoice scans to fill them automatically',
    'depends': ['account', 'iap_mail', 'mail_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/config_parameter_endpoint.xml',
        'data/extraction_status.xml',
        'data/res_config_settings_views.xml',
        'data/crons.xml',
        'views/account_move_views.xml',
    ],
    'auto_install': True,
    'license': 'OEEL-1',
    'assets': {
        'web.assets_backend': [
            'account_invoice_extract/static/src/js/*.js',
            'account_invoice_extract/static/src/css/*.css',
            'account_invoice_extract/static/src/xml/*.xml',
        ],
        'web.qunit_suite_tests': [
            'account_invoice_extract/static/src/tests/helpers/*',
            'account_invoice_extract/static/src/tests/*',
        ],
    }
}
