# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

import swiss.tests


@swiss.tests.tagged('post_install', '-at_install')
class TestUi(swiss.tests.HttpCase):

    def test_01_mail_tour(self):
        self.start_tour("/web", 'mail_tour', login="admin")
