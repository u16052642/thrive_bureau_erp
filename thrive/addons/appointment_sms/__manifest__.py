# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Appointment SMS',
    'version': '1.0',
    'category': 'Marketing/Online Appointment',
    'sequence': 2150,
    'summary': 'Use SMS reminders for appointment meetings',
    'website': 'https://www.ThriveERP.com/app/appointments',
    'description': """Enable sending appointment reminders via SMS to your clients.""",
    'depends': ['appointment', 'calendar_sms'],
    'data': [
        'data/calendar_data.xml',
        'views/appointment_templates_registration.xml',
    ],
    'demo': [
        'data/appointment_demo.xml',
    ],
    'auto_install': True,
    'license': 'OEEL-1',
}
