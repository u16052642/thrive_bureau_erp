# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, api


class StockLot(models.Model):
    _inherit = 'stock.lot'
    _barcode_field = 'name'

    def _get_stock_barcode_specific_data(self):
        products = self.product_id
        return {
            'product.product': products.read(self.env['product.product']._get_fields_stock_barcode(), load=False),
            'uom.uom': products.uom_id.read(self.env['uom.uom']._get_fields_stock_barcode(), load=False)
        }

    @api.model
    def _get_fields_stock_barcode(self):
        return ['name', 'ref', 'product_id']
