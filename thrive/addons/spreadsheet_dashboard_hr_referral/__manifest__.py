# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': "Spreadsheet dashboard for recruitment",
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Spreadsheet',
    'description': 'Spreadsheet',
    'depends': ['spreadsheet_dashboard', 'hr_referral'],
    'data': [
        "data/dashboards.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': ['hr_referral'],
    'license': 'OEEL-1',
    'assets': {}
}
