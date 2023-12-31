# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.


{
    'name': 'Website Appointments',
    'version': '1.0',
    'category': 'Marketing/Online Appointment',
    'sequence': 215,
    'website': 'https://www.thrivebureau.com/page/appointments',
    'description': """
Allow clients to Schedule Appointments through your Website
-------------------------------------------------------------

""",
    'depends': ['appointment', 'website_enterprise', 'website_partner'],
    'data': [
        'data/calendar_data.xml',
        'data/website_data.xml',
        'views/appointment_type_views.xml',
        'views/calendar_menus.xml',
        'views/appointment_templates_appointments.xml',
        'views/appointment_templates_registration.xml',
        'views/appointment_templates_validation.xml',
        'views/website_pages_views.xml',
        'security/calendar_security.xml',
        'security/ir.model.access.csv',
        'views/snippets.xml',
    ],
    'demo': [
        'data/appointment_demo.xml',
    ],
    'installable': True,
    'auto_install': ['appointment', 'website_enterprise'],
    'license': 'OEEL-1',
    'assets': {
        'web.assets_tests': [
            'website_appointment/static/tests/tours/*',
        ],
        'web.assets_frontend': [
            'website_appointment/static/src/scss/website_appointment.scss',
            'website_appointment/static/src/scss/website_appointment_editor.scss',
            'website_appointment/static/src/xml/website_appointment_templates.xml',
            'website_appointment/static/src/xml/appointment_no_slot.xml',
        ],
        'website.assets_editor': [
            'website_appointment/static/src/js/systray_items/*.js',
        ],
    }
}
