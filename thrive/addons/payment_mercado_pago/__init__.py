# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models

from thrive.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(cr, registry):
    setup_provider(cr, registry, 'mercado_pago')


def uninstall_hook(cr, registry):
    reset_payment_provider(cr, registry, 'mercado_pago')