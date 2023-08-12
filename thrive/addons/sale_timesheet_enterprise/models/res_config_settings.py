# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields

from thrive.addons.sale_timesheet_enterprise.models.sale import DEFAULT_INVOICED_TIMESHEET


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoiced_timesheet = fields.Selection([
        ('all', "All recorded timesheets"),
        ('approved', "Validated timesheets only"),
    ], default=DEFAULT_INVOICED_TIMESHEET, string="Timesheets Invoicing", config_parameter='sale.invoiced_timesheet',
        help="With the 'all recorded timesheets' option, all timesheets will be invoiced without distinction, even if they haven't been validated."
        " Additionally, all timesheets will be accessible in your customers' portal. \n"
        "When you choose the 'validated timesheets only' option, only the validated timesheets will be invoiced and appear in your customers' portal.")

    def set_values(self):
        """ Override set_values to recompute the qty_delivered for each sale.order.line
            where :
                -   the sale.order has the state to 'sale',
                -   the type of the product is a 'service',
                -   the service_policy in product has 'delivered_timesheet'.

            We need to recompute this field because when the invoiced_timesheet
            config changes, this field isn't recompute.
            When the qty_delivered field is recomputed, we need to update the
            qty_to_invoice and invoice status fields.
        """
        old_value = self.env["ir.config_parameter"].sudo().get_param("sale.invoiced_timesheet")
        if old_value and self.invoiced_timesheet != old_value:
            # recompute the qty_delivered in sale.order.line for sale.order
            # where his state is set to 'sale'.
            sale_order_lines = self.env['sale.order.line'].sudo().search([
                ('state', 'in', ['sale', 'done']),
                ('invoice_status', 'in', ['no', 'to invoice']),
                ('product_id.type', '=', 'service'),
                ('product_id.service_type', '=', 'timesheet'),
            ])

            if sale_order_lines:
                sale_order_lines._compute_qty_delivered()
                sale_order_lines._compute_qty_to_invoice()
                sale_order_lines._compute_invoice_status()
        return super().set_values()
