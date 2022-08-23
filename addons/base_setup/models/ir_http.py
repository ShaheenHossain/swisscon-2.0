# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.
from swiss import models
from swiss.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        if request.env.user.has_group('base.group_user'):
            result['show_effect'] = request.env['ir.config_parameter'].sudo().get_param('base_setup.show_effect')
        return result
