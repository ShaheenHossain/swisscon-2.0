# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.
from swiss import fields, models


class City(models.Model):
    _inherit = "res.city"

    l10n_pe_code = fields.Char('Code', help='This code will help with the '
                               'identification of each city in Peru.')
