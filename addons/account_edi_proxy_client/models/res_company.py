# -*- coding:utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.
from swiss import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_edi_proxy_client_ids = fields.One2many('account_edi_proxy_client.user', inverse_name='company_id')
