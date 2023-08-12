# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Documents - Project - Sale',
    'version': '1.0',
    'category': 'Productivity/Documents',
    'summary': 'Products Workspace Templates',
    'description': """
Adds the ability to set workspace templates on products.
""",
    'depends': ['documents_project', 'sale_project'],
    'data': [
        'views/product_views.xml',
    ],
    'demo': [
        'data/documents_project_sale_demo.xml',
    ],
    'auto_install': True,
    'license': 'OEEL-1',
}
