# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from thrive import models, fields, _
from thrive.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_in_gstr_gst_username = fields.Char(
        "GST username", related="company_id.l10n_in_gstr_gst_username", readonly=False
    )
    l10n_in_gstr_gst_otp = fields.Char("OTP")
    l10n_in_gstr_gst_token = fields.Char("GST Token", readonly=True)
    l10n_in_gstr_gst_auto_refresh_token = fields.Boolean(
        string="Is auto refresh token",
        related="company_id.l10n_in_gstr_gst_auto_refresh_token",
        readonly=False)
    l10n_in_gstr_gst_production_env = fields.Boolean(
        string="Indian GST Testing Environment",
        related="company_id.l10n_in_gstr_gst_production_env",
        readonly=False
    )

    def l10n_in_gstr_gst_send_otp(self):
        response = self.env["l10n_in.gst.return.period"]._otp_request(self.company_id)
        if response.get('error'):
            error_message = "\n".join(["[%s] %s"%(error.get('code'), error.get('message')) for error in response.get("error", {})])
            raise UserError(error_message)
        context = {
            "default_l10n_in_gstr_gst_token": response.get("txn"),
            "default_company_id": self.company_id.id,
        }
        form = self.env.ref("l10n_in_reports_gstr.view_get_otp_validate_wizard")
        return {
            "name": _("Otp Request"),
            "type": "ir.actions.act_window",
            "res_model": "res.config.settings",
            "views": [[form.id, "form"]],
            "target": "new",
            "context": context,
        }

    def l10n_in_gstr_validate_otp(self):
        response = self.env["l10n_in.gst.return.period"]._otp_auth_request(
            company=self.company_id, transaction=self.l10n_in_gstr_gst_token, otp=self.l10n_in_gstr_gst_otp)
        if response.get('error'):
            error_codes = [e.get('code') for e in response["error"]]
            if 'AUTH4033' in error_codes:
                raise UserError(_("Invalid OTP"))
            message = "\n".join(["[%s] %s"%(e.get('code'), e.get('message')) for e in response["error"]])
            raise UserError(_('%s', message))
        self.company_id.write({
            "l10n_in_gstr_gst_token": self.l10n_in_gstr_gst_token,
            "l10n_in_gstr_gst_token_validity": fields.Datetime.now() + timedelta(hours=6)
        })
