# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

import json
import logging
import pprint

from swiss import http
from swiss.http import request

_logger = logging.getLogger(__name__)


class SwissCRMByAdyenController(http.Controller):
    _notification_url = '/payment/swiss_adyen/notification'

    @http.route('/payment/swiss_adyen/notification', type='json', auth='public', csrf=False)
    def swiss_adyen_notification(self):
        data = json.loads(request.httprequest.data)
        _logger.info('Beginning SwissCRM by Adyen form_feedback with data %s', pprint.pformat(data)) 
        if data.get('authResult') not in ['CANCELLED']:
            request.env['payment.transaction'].sudo().form_feedback(data, 'swiss_adyen')
