from thrive import fields, models

class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    product_id = fields.Many2one(domain="[('sale_ok', '=', True), ('detailed_type', 'not in', ['event', 'event_booth']), ('company_id', 'in', [company_id, False])]")
