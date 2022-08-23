# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss import fields, models


class TrackTagCategory(models.Model):
    _name = "event.track.tag.category"
    _description = 'Event Track Tag Category'
    _order = "sequence"

    name = fields.Char("Name", required=True, translate=True)
    sequence = fields.Integer('Sequence', default=10)
    tag_ids = fields.One2many('event.track.tag', 'category_id', string="Tags")
