# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from swiss.addons.website_event.controllers.main import WebsiteEventController


class EventOnlineController(WebsiteEventController):

    def _get_registration_confirm_values(self, event, attendees_sudo):
        values = super(EventOnlineController, self)._get_registration_confirm_values(event, attendees_sudo)
        values['hide_sponsors'] = True
        return values
