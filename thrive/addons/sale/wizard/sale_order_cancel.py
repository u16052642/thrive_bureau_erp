# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, api, fields, models
from thrive.exceptions import UserError
from thrive.tools import formataddr


class SaleOrderCancel(models.TransientModel):
    _name = 'sale.order.cancel'
    _inherit = 'mail.composer.mixin'
    _description = "Sales Order Cancel"

    @api.model
    def _default_email_from(self):
        if self.env.user.email:
            return formataddr((self.env.user.name, self.env.user.email))
        raise UserError(_("Unable to post message, please configure the sender's email address."))

    @api.model
    def _default_author_id(self):
        return self.env.user.partner_id

    # origin
    email_from = fields.Char(string="From", default=_default_email_from)
    author_id = fields.Many2one(
        'res.partner',
        string="Author",
        index=True,
        ondelete='set null',
        default=_default_author_id,
    )

    # recipients
    recipient_ids = fields.Many2many(
        'res.partner',
        string="Recipients",
        compute='_compute_recipient_ids',
        readonly=False,
    )
    order_id = fields.Many2one('sale.order', string="Sale Order", required=True, ondelete='cascade')
    display_invoice_alert = fields.Boolean(
        string="Invoice Alert",
        compute='_compute_display_invoice_alert',
    )

    @api.depends('order_id')
    def _compute_recipient_ids(self):
        for wizard in self:
            wizard.recipient_ids = wizard.order_id.partner_id \
                                   | wizard.order_id.message_partner_ids \
                                   - wizard.author_id

    @api.depends('order_id')
    def _compute_display_invoice_alert(self):
        for wizard in self:
            wizard.display_invoice_alert = bool(
                wizard.order_id.invoice_ids.filtered(lambda inv: inv.state == 'draft')
            )

    @api.depends('order_id')
    def _compute_subject(self):
        for wizard in self:
            if wizard.template_id:
                wizard.subject = self.sudo()._render_template(
                    wizard.template_id.subject,
                    'sale.order',
                    [wizard.order_id.id],
                    post_process=True,
                )[wizard.order_id.id]

    @api.depends('order_id')
    def _compute_body(self):
        for wizard in self:
            if wizard.template_id:
                wizard.body = self.sudo()._render_template(
                    wizard.template_id.body_html,
                    'sale.order',
                    [wizard.order_id.id],
                    post_process=True,
                    engine='qweb',
                )[wizard.order_id.id]

    def action_send_mail_and_cancel(self):
        self.ensure_one()
        self.order_id.message_post(
            subject=self.subject,
            body=self.body,
            message_type='comment',
            email_from=self.email_from,
            email_layout_xmlid='mail.mail_notification_light',
            partner_ids=self.recipient_ids.ids,
        )
        return self.action_cancel()

    def action_cancel(self):
        return self.order_id.with_context({'disable_cancel_warning': True}).action_cancel()
