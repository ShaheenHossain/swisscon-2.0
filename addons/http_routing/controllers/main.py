# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import http
from swiss.http import request
from swiss.addons.web.controllers.main import WebClient, Home


class Routing(Home):

    @http.route('/website/translations/<string:unique>', type='http', auth="public", website=True)
    def get_website_translations(self, unique, lang, mods=None):
        IrHttp = request.env['ir.http'].sudo()
        modules = IrHttp.get_translation_frontend_modules()
        if mods:
            modules += mods.split(',') if isinstance(mods, str) else mods
        return WebClient().translations(unique, mods=','.join(modules), lang=lang)
