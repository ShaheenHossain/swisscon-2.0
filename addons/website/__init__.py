# -*- encoding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models
from . import wizard

import swiss
from swiss import api, SUPERUSER_ID
from functools import partial


def uninstall_hook(cr, registry):
    def rem_website_id_null(dbname):
        db_registry = swiss.modules.registry.Registry.new(dbname)
        with api.Environment.manage(), db_registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            env['ir.model.fields'].search([
                ('name', '=', 'website_id'),
                ('model', '=', 'res.config.settings'),
            ]).unlink()

    cr.postcommit.add(partial(rem_website_id_null, cr.dbname))


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.module.module'].update_theme_images()
