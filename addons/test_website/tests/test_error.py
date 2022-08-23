import swiss.tests
from swiss.tools import mute_logger


@swiss.tests.common.tagged('post_install', '-at_install')
class TestWebsiteError(swiss.tests.HttpCase):

    @mute_logger('swiss.addons.http_routing.models.ir_http', 'swiss.http')
    def test_01_run_test(self):
        self.start_tour("/test_error_view", 'test_error_website')
