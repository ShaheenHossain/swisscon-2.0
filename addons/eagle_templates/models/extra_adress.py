from swiss import fields, models, api


class ExtraAddress(models.Model):
    _inherit = 'res.company'

    eu_vat_id_no = fields.Char(string='EU-MwSt.-IdNr:')
    eu_vat_id_no_02 = fields.Char(string='EU-MwSt.-IdNr:')
    district_court = fields.Char(string='Bezirksgericht:')
    commercial_register = fields.Char(string='Handelsregister:')
    bank_name = fields.Char(string='Bank:')
    blz = fields.Char(string='BLZ')
    account_no = fields.Char(string='Kontonr:')
    account_owner = fields.Char(string='Kontoinhaber:')
    bic = fields.Char(string='BIC:')
    iban_no = fields.Char(string='IBAN:')


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    eu_vat_id_no = fields.Char(string='EU-MwSt.-IdNr:')
    eu_vat_id_no_02 = fields.Char(string='EU-MwSt.-IdNr:')
    district_court = fields.Char(string='Bezirksgericht:')
    commercial_register = fields.Char(string='Handelsregister:')
    bank_name = fields.Char(string='Bank:')
    blz = fields.Char(string='BLZ')
    account_no = fields.Char(string='Kontonr:')
    account_owner = fields.Char(string='Kontoinhaber:')
    bic = fields.Char(string='BIC:')
    iban_no = fields.Char(string='IBAN:')