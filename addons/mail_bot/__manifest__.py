# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'SwissCRMBot',
    'version': '1.2',
    'category': 'Productivity/Discuss',
    'summary': 'Add SwissCRMBot in discussions',
    'description': "",
    'website': 'https://www.swissconsultings.ch/page/discuss',
    'depends': ['mail'],
    'auto_install': True,
    'installable': True,
    'application': False,
    'data': [
        'views/assets.xml',
        'views/res_users_views.xml',
        'data/mailbot_data.xml',
    ],
    'demo': [
        'data/mailbot_demo.xml',
    ],
    'qweb': [
        'static/src/bugfix/bugfix.xml',
    ],
    'license': 'LGPL-3',
}
