# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    "name": """Mexico - Electronic Delivery Guide Comex""",
    'version': '1.0.',
    'category': 'Accounting/Localizations/EDI',
    'description': """
    Bridge module to extend the delivery guide (Complemento XML Carta de Porte)
    - exported goods (COMEX)
    - extended address fields
    """,
    'depends': [
        'l10n_mx_edi_extended',
        'l10n_mx_edi_stock',
    ],
    'demo': [
        'demo/res_partner.xml',
    ],
    'data': [
        'data/cfdi_cartaporte.xml',
        'views/stock_picking_views.xml',
        'views/report_deliveryslip.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
