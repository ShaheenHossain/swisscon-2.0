# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    plan_to_change_car = fields.Boolean('Plan To Change Car', default=False)
