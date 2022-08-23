# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Budget Management',
    'author': 'SwissCRM , Odoo Mates, Odoo SA',
    'category': 'Accounting',
    'version': '2.0.1.0.0',
    'description': """Use budgets to compare actual with expected revenues and costs""",
    'summary': 'Budget Management',
    'sequence': 10,
    'website': 'https://www.swisshq.com',
    'depends': ['account'],
    'license': 'LGPL-3',
    'company': 'SwissCRM ',
    'maintainer': 'SwissCRM ',
    'data': [
        'security/ir.model.access.csv',
        'security/account_budget_security.xml',
        'views/account_analytic_account_views.xml',
        'views/account_budget_views.xml',
        'views/res_config_settings_views.xml',
    ],
    "images": ['static/description/banner.gif'],
    'demo': ['data/account_budget_demo.xml'],
}
