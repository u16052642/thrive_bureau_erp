# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Documents - Payroll',
    'version': '1.0',
    'category': 'Productivity/Documents',
    'summary': 'Store employee payslips in the Document app',
    'description': """
Employee payslips will be automatically integrated to the Document app.
""",
    'website': ' ',
    'depends': ['documents_hr', 'hr_payroll'],
    'data': [
        'data/data.xml',
        'views/documents_views.xml',
        'security/security.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
