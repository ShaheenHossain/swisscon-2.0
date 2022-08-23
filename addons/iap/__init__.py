# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from . import models
from . import tools

# compatibility imports
from swiss.addons.iap.tools.iap_tools import iap_jsonrpc as jsonrpc
from swiss.addons.iap.tools.iap_tools import iap_authorize as authorize
from swiss.addons.iap.tools.iap_tools import iap_cancel as cancel
from swiss.addons.iap.tools.iap_tools import iap_capture as capture
from swiss.addons.iap.tools.iap_tools import iap_charge as charge
from swiss.addons.iap.tools.iap_tools import InsufficientCreditError
