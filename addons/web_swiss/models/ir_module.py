from swiss import api, fields, models, modules, tools, _

class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    license = fields.Selection(selection_add=[('FPL-1', 'SwissCRM Proprietary License v1.0'),
                                              ('FPEL-1', 'SwissCRM Professional Edition License v1.0'),
                                              ])
