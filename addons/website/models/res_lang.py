# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import api, models, tools, _
from swiss.addons.website.models import ir_http
from swiss.exceptions import UserError
from swiss.http import request


class Lang(models.Model):
    _inherit = "res.lang"

    def write(self, vals):
        if 'active' in vals and not vals['active']:
            if self.env['website'].search([('language_ids', 'in', self._ids)]):
                raise UserError(_("Cannot deactivate a language that is currently used on a website."))
        return super(Lang, self).write(vals)

    @api.model
    @tools.ormcache_context(keys=("website_id",))
    def get_available(self):
        website = ir_http.get_request_website()
        if not website:
            return super().get_available()
        # Return the website-available ones in this case
        return request.website.language_ids.get_sorted()
