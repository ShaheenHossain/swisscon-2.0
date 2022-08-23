# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import api, models, fields


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    @api.model
    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        journal_data = super(AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict)
        for journal in journal_data:
            if journal['type'] in ('sale', 'purchase') and company.country_id.code == "BE":
                journal.update({'refund_sequence': True})
        return journal_data
