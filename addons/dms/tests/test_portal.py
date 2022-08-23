# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import swiss.tests


@swiss.tests.tagged("post_install", "-at_install")
class TestDmsPortal(swiss.tests.HttpCase):
    def test_tour(self):
        self.start_tour(
            "/",
            "swiss.__DEBUG__.services['web_tour.tour'].run('dms_portal_tour')",
            "swiss.__DEBUG__.services['web_tour.tour'].tours.dms_portal_tour.ready",
            login="portal",
        )
