# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_code = fields.Char(
        string="HS Code",
        help="Standardized code for international shipping and goods declaration. At the moment, only used for the FedEx shipping provider.",
    )
