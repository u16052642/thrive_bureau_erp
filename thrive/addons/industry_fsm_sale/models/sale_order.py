# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    task_id = fields.Many2one('project.task', string="Task", help="Task from which this quotation have been created")

    @api.model_create_multi
    def create(self, vals):
        orders = super().create(vals)
        for sale_order in orders:
            if sale_order.task_id:
                message = _(
                    "Quotation created: %s",
                    sale_order._get_html_link())
                sale_order.task_id.message_post(body=message)
        return orders

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('fsm_no_message_post'):
            return False
        return super().message_post(**kwargs)


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    delivered_price_subtotal = fields.Monetary(compute='_compute_delivered_amount', string='Delivered Subtotal')
    delivered_price_tax = fields.Float(compute='_compute_delivered_amount', string='Delivered Total Tax')
    delivered_price_total = fields.Monetary(compute='_compute_delivered_amount', string='Delivered Total')

    @api.depends('qty_delivered', 'discount', 'price_unit', 'tax_id')
    def _compute_delivered_amount(self):
        """
        Compute the amounts of the SO line for delivered quantity.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.qty_delivered, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.delivered_price_tax = sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
            line.delivered_price_total = taxes['total_included']
            line.delivered_price_subtotal = taxes['total_excluded']

    def _timesheet_create_task_prepare_values(self, project):
        res = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        if project.is_fsm:
            res.update({'partner_id': self.order_id.partner_shipping_id.id})
        return res

    def _timesheet_create_project_prepare_values(self):
        """Generate project values"""
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        if self.product_id.project_template_id.is_fsm:
            values.pop('sale_line_id', False)
        return values
