# -*- coding: utf-8 -*-

import swiss

def migrate(cr, version):
    registry = swiss.registry(cr.dbname)
    from swiss.addons.account.models.chart_template import migrate_set_tags_and_taxes_updatable
    migrate_set_tags_and_taxes_updatable(cr, registry, 'l10n_hr')
