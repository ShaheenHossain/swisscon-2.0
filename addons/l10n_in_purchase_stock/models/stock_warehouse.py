# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import models, fields, api


class Stock(models.Model):
    _inherit = 'stock.warehouse'

    l10n_in_purchase_journal_id = fields.Many2one('account.journal', string="Purchase Journal")
