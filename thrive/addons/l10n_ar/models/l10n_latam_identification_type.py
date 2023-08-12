# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive import models, fields


class L10nLatamIdentificationType(models.Model):

    _inherit = "l10n_latam.identification.type"

    l10n_ar_afip_code = fields.Char("AFIP Code")