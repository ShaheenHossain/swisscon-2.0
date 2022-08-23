# Part of SwissCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Invoice Recurrings',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Create recurring of invoices',
    'description': """
    Account Invoice Recurring allows to automatically create
    recurring of any particular invoice
    """,
    'author': 'SwissCRM ',
    'website': 'https://www.swisshq.com/',
    'depends': ['account', 'recurring'],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
