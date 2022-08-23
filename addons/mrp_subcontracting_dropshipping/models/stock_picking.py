# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_warehouse(self, subcontract_move):
        if subcontract_move.sale_line_id:
            return subcontract_move.sale_line_id.order_id.warehouse_id
        return super(StockPicking, self)._get_warehouse(subcontract_move)
