# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, fields, models, _
from thrive.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # l10n_de_datev_identifier now only targets vendors instead of all partners
    l10n_de_datev_identifier = fields.Integer(
        string='DateV Vendor',
        help="In the DateV export of the General Ledger, each vendor will be identified by this identifier. "
        "If this identifier is not set, the database id of the partner will be added to a multiple of ten starting by the number 7."
        "The account code's length can be specified in the company settings."
    )
    l10n_de_datev_identifier_customer = fields.Integer(
        string='DateV Customer',
        copy=False,
        tracking=True,
        compute="_compute_l10n_de_datev_identifier_customer", store=True, readonly=False,
        help="In the DateV export of the General Ledger, each customer will be identified by this identifier. "
        "If this identifier is not set, the database id of the partner will be added to a multiple of ten starting by the number 1."
        "The account code's length can be specified in the company settings."
    )

    @api.constrains('l10n_de_datev_identifier_customer')
    def _check_datev_identifier_customer(self):
        self.flush_model(['l10n_de_datev_identifier_customer'])
        self.env.cr.execute("""
            SELECT COUNT(id), l10n_de_datev_identifier_customer FROM res_partner
            WHERE l10n_de_datev_identifier_customer != 0
            GROUP BY l10n_de_datev_identifier_customer
            HAVING COUNT(id) > 1
        """)

        if self.env.cr.dictfetchone():
            raise ValidationError(_('You have already defined a partner with the same Datev Customer identifier'))

    def _compute_l10n_de_datev_identifier_customer(self):
        # Compute without depends so it is only computed when installing the module
        for partner in self:
            partner.l10n_de_datev_identifier_customer = partner.l10n_de_datev_identifier
