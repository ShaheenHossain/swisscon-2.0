# Part of SwissCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Order Recurring',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Create recurring of purchase order',
    'description': """
    Purchase Order Recurring allows to automatically create recurring of
    any particular purchase order
    """,
    'author': 'SwissCRM ',
    'website': 'https://www.swissconsultings.ch/',
    'depends': ['recurring', 'purchase', 'sale_purchase'],
    'data': [
        'views/purchase_views.xml',
    ],
    'demo': ['demo/purchase_recurring_demo.xml'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
