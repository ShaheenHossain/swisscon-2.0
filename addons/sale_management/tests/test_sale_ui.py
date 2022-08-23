import swiss.tests
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.


@swiss.tests.tagged('post_install', '-at_install')
class TestUi(swiss.tests.HttpCase):

    def test_01_sale_tour(self):
        self.start_tour("/web", 'sale_tour', login="admin", step_delay=100)
