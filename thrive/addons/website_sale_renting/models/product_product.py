# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _website_show_quick_add(self):
        self.ensure_one()
        return not self.rent_ok and super()._website_show_quick_add()
