# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

import swiss.tests
from swiss.tools import mute_logger


@swiss.tests.common.tagged('post_install', '-at_install')
class TestCustomSnippet(swiss.tests.HttpCase):

    @mute_logger('swiss.addons.http_routing.models.ir_http', 'swiss.http')
    def test_01_run_tour(self):
        self.start_tour("/", 'test_custom_snippet', login="admin")
