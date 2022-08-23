import swiss.tests
from swiss.tools import mute_logger


@swiss.tests.common.tagged('post_install', '-at_install')
class TestWebsiteSession(swiss.tests.HttpCase):

    def test_01_run_test(self):
        self.start_tour('/', 'test_json_auth')
