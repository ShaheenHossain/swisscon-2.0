from swiss import api, SUPERUSER_ID

from . import models
from . import controllers

XML_ID = "web_swiss._assets_primary_variables"
SCSS_URL = '/web_swiss/static/src/scss/backend_theme_customizer/colors.scss'


def _uninstall_reset_changes(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['web_swiss.scss_editor'].reset_values(SCSS_URL, XML_ID)
