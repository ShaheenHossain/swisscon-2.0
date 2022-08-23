# -*- coding: ascii -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import api, models
from swiss.addons.http_routing.models.ir_http import slug, unslug_url


class IrUiView(models.Model):
    _inherit = ["ir.ui.view"]

    @api.model
    def _prepare_qcontext(self):
        qcontext = super(IrUiView, self)._prepare_qcontext()
        qcontext['slug'] = slug
        qcontext['unslug_url'] = unslug_url
        return qcontext
