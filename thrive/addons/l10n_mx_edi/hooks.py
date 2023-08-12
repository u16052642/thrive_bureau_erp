# coding: utf-8
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # UNSPSC category codes can be used in Mexico.
    product_unspsc = env['product.unspsc.code'].search([('active', '=', False), ('code', '=ilike', '%00')])
    product_unspsc.active = True
