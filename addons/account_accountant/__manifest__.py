# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting',
    'version': '2.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Accounting Reports, Asset Management and Account Budget For SwissCRM Community Edition',
    'sequence': '1',
    'website': 'https://www.swisshq.com',
    'author': 'SwissCRM , Odoo Mates, Odoo SA',
    'company': 'SwissCRM ',
    'maintainer': 'SwissCRM ',
    'license': 'LGPL-3',
    'depends': ['web_swiss','accounting_pdf_reports', 'account_asset',
                'account_budget'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'security/account_security.xml',
        'views/account.xml',
        'views/account_type.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'qweb': [],
}
