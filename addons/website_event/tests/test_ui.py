# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

import swiss.tests
from swiss import tools


@swiss.tests.tagged('post_install', '-at_install')
class TestUi(swiss.tests.HttpCase):
    def test_admin(self):
        self.start_tour("/", 'event', login='admin', step_delay=100)
