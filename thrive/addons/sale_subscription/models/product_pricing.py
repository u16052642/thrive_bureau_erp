# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models, _
from thrive.exceptions import ValidationError

class ProductPricing(models.Model):
    _inherit = 'product.pricing'

    @api.constrains('product_template_id', 'recurrence_id')
    def _check_invalid_units_not_used(self):
        for pricing in self:
            if pricing.recurrence_id.unit in ['hour', 'day'] and pricing.product_template_id.recurring_invoice:
                raise ValidationError(_("Hourly and daily pricing are forbidden on recurring products"))
