# Part of swiss See LICENSE file for full copyright and licensing details.

{
    'name': 'Helpdesk Forum',
    'version': '1.0',
    'summary': '''Helpdesk Forum will provide you forum per
helpdesk team''',
    'category': 'Human Resources',
    'author': 'SwissCRM ',
    'website': 'https://swissconsultings.ch',
    'depends': ['helpdesk_basic', 'website_forum'],
    'data': [
        'views/helpdesk_team_view.xml',
        'views/helpdesk_ticket_view.xml',
    ],
    
    'installable': True,
    'auto_install': False,
}
