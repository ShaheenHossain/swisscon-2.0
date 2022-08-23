# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _needs_automatic_assign(self):
        self.ensure_one()
        if self.sale_id:
            return True
        return super()._needs_automatic_assign()
