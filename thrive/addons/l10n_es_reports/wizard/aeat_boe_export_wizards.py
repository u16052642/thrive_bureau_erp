# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields, api, _

from thrive.exceptions import ValidationError, UserError

import json

import re

class AEATBOEExportWizard(models.TransientModel):
    _name = 'l10n_es_reports.aeat.boe.export.wizard'
    _description = "BOE Export Wizard"

    report_id = fields.Many2one(string="Report", comodel_name='account.report', required=True)
    calling_export_wizard_id = fields.Many2one(string="Calling Export Wizard", comodel_name="account_reports.export.wizard", help="Optional field containing the report export wizard calling this BOE wizard, if there is one.")

    def download_boe_action(self):
        if not self.env.company.vat:
            raise UserError(_("Please first set the TIN of your company."))

        if self.calling_export_wizard_id and not self.calling_export_wizard_id.l10n_es_reports_boe_wizard_model:
            # In this case, the BOE wizard has been called by an export wizard, and this wizard has not yet received the data necessary to generate the file
            self.calling_export_wizard_id.l10n_es_reports_boe_wizard_id = self.id
            self.calling_export_wizard_id.l10n_es_reports_boe_wizard_model = self._name
            return self.calling_export_wizard_id.export_report()
        else:
            options = self.env.context.get('l10n_es_reports_report_options', {})
            return self.report_id.export_file({**options, 'l10n_es_reports_boe_wizard_id': self.id}, 'export_boe')

class Mod111And115And303CommonBOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod111and115and303.export.wizard'
    _description = "BOE Export Wizard for (mod111, mod115 & 303)"

    def _get_current_company(self):
        return self.env.company

    company_id = fields.Many2one(string="Current Company", comodel_name='res.company', default=_get_current_company)
    company_partner_id = fields.Many2one(string="Company Partner", comodel_name='res.partner', related='company_id.partner_id', readonly=False)
    partner_bank_id = fields.Many2one(string="Direct Debit Account", comodel_name='res.partner.bank', help="The IBAN account number to use for direct debit. Leave blank if you don't use direct debit.", domain="[('partner_id','=',company_partner_id)]")
    complementary_declaration = fields.Boolean(string="Complementary Declaration", help="Whether or not this BOE file is a complementary declaration.")
    declaration_type = fields.Selection(string="Declaration Type", selection=[('I', 'I - Income'), ('U', 'U - Direct debit'), ('G', 'G - Income to enter on CCT'), ('N', 'N - To return')], required=True, default='I')
    previous_report_number = fields.Char(string="Previous Report Number", size=13, help="Number of the report previously submitted")

    @api.constrains('partner_bank_id')
    def validate_partner_bank_id(self):
        for record in self:
            if record.partner_bank_id.acc_type != 'iban':
                raise ValidationError(_("Please select an IBAN account."))


class Mod347And349CommonBOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod347and349.export.wizard'
    _description = "BOE Export Wizard for (mod347 & mod349)"

    def _default_contact_name(self):
        return self.env.user.name

    def _default_contact_phone(self):
        return self.env.user.partner_id.phone

    contact_person_name = fields.Char(string="Contact person", default=_default_contact_name, required=True, help="Name of the contact person fot this BOE file's submission")
    contact_person_phone = fields.Char(string="Contact phone number", default=_default_contact_phone, help="Phone number where to join the contact person")
    complementary_declaration = fields.Boolean(string="Complementary Declaration", help="Whether or not this BOE file corresponds to a complementary declaration")
    substitutive_declaration = fields.Boolean(string="Substitutive Declaration", help="Whether or not this BOE file corresponds to a substitutive declaration")
    previous_report_number = fields.Char(string="Previous Report Number", size=13, help="Number of the previous report, corrected or replaced by this one, if any")

    def get_formatted_contact_phone(self):
        return re.sub('\D', '', self.contact_person_phone or '')


class Mod111BOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.mod111and115and303.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod111.export.wizard'
    _description = "BOE Export Wizard for (mod111)"

    MODELO_NUMBER = 111

    # No field, but keeping it so is mandatory for the genericity of the modelling


class Mod115BOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.mod111and115and303.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod115.export.wizard'
    _description = "BOE Export Wizard for (mod115)"

    MODELO_NUMBER = 115

    # No field, but keeping it so is mandatory for the genericity of the modelling


class Mod303BOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.mod111and115and303.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod303.export.wizard'
    _description = "BOE Export Wizard for (mod303)"

    MODELO_NUMBER = 303

    monthly_return = fields.Boolean(string="In Monthly Return Register")
    using_sii = fields.Boolean(string="Using SII Voluntarily", default=False)
    exempted_from_mod_390 = fields.Boolean(string="Exempted From Modelo 390", default=False)
    exempted_from_mod_390_available = fields.Boolean(compute='_compute_show_exempted_from_mod_390', help="Technical field used to only make exempted_from_mod_390 avilable in the last period (12 or 4T)")

    def _compute_show_exempted_from_mod_390(self):
        report = self.env.ref('l10n_es_reports.mod_303')
        options = self.env.context.get('l10n_es_reports_report_options', {})
        period = self.env[report.custom_handler_model_name]._get_mod_period_and_year(options)[0]
        for record in self:
            record.exempted_from_mod_390_available = period in ('12', '4T')

    @api.constrains('partner_bank_id')
    def validate_bic(self):
        for record in self:
            if not record.partner_bank_id.bank_bic:
                raise ValidationError(_("Please first assign a BIC number to the bank related to this account."))

    def _get_using_sii_2021_value(self):
        return 1 if self.using_sii else 2

    def _get_exonerated_from_mod_390_2021_value(self, period):
        if period in ('12', '4T'):
            return 1 if self.exempted_from_mod_390 else 2
        return 0

class Mod347BOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.mod347and349.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod347.export.wizard'
    _description = "BOE Export Wizard for (mod347)"

    MODELO_NUMBER = 347

    cash_basis_mod347_data = fields.One2many(
        comodel_name='l10n_es_reports.aeat.mod347.manual.partner.data',
        inverse_name='parent_wizard_id',
        string="Cash Basis Data",
        help="Manual entries containing the amounts perceived for the partners with cash basis criterion during this year. Leave empty for partners for which this criterion does not apply.")

    def l10n_es_get_partners_manual_parameters_map(self):
        cash_basis_dict = {}
        for data in self.cash_basis_mod347_data:
            if not cash_basis_dict.get(data.partner_id.id):
                cash_basis_dict[data.partner_id.id] = {'local_negocio': {'A': None, 'B':None}, 'seguros': {'B': None}, 'otras': {'A': None, 'B': None}}

            cash_basis_dict[data.partner_id.id][data.operation_class][data.operation_key] = data.perceived_amount

        return {'cash_basis': cash_basis_dict}


class Mod347BOEManuaPartnerData(models.TransientModel):
    _name = 'l10n_es_reports.aeat.mod347.manual.partner.data'
    _description = "Manually Entered Data for Mod 347 Report"

    parent_wizard_id = fields.Many2one(comodel_name='l10n_es_reports.aeat.boe.mod347.export.wizard')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    perceived_amount = fields.Monetary(string='Perceived Amount', required=True)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', default=lambda self: self.env.company.currency_id) #required by the monetary field
    operation_key = fields.Selection(selection=[('A', 'Adquisiciones de bienes y servicios'),('B', 'Entregas de bienes y prestaciones de servicios')], required=True, string='Operation Key')
    operation_class = fields.Selection(selection=[('local_negocio', 'Arrendamiento Local Negocio'), ('seguros', 'Operaciones de Seguros'), ('otras', 'Otras operaciones')], required=True, string='Operation Class')


class Mod349BOEWizard(models.TransientModel):
    _inherit = 'l10n_es_reports.aeat.boe.mod347and349.export.wizard'
    _name = 'l10n_es_reports.aeat.boe.mod349.export.wizard'
    _description = "BOE Export Wizard for (mod349)"

    MODELO_NUMBER = 349

    trimester_2months_report = fields.Boolean(string="Trimester monthly report", help="Whether or not this BOE file must be generated with the data of the first two months of the trimester (in case its total amount of operation is above the threshold fixed by the law)")
