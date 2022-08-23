# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    adyen_account_id = fields.Many2one('adyen.account', string='Adyen Account', readonly=True)
