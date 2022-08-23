# Part of swiss. See LICENSE file for full copyright and licensing details.

from swiss import fields, models


class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    elearning_id = fields.Many2one('slide.channel', string="E Learning")
