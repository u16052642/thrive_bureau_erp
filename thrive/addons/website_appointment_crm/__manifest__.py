# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Appointment Lead Enrichment',
    'version': '1.0',
    'category': 'Marketing/Online Appointment',
    'sequence': 2160,
    'summary': 'Enrich lead created automatically through an appointment with gathered website visitor information',
    'website': 'https://www.ThriveERP.com/app/appointments',
    'description': """
Enrich lead created automatically through an appointment with gathered website visitor information such as language, 
country and detailed information like pages browsed by the lead (through a link to website visitor).
""",
    'depends': ['appointment_crm', 'website_crm'],
    'data': [
    ],
    'application': False,
    'auto_install': True,
    'license': 'OEEL-1',
}
