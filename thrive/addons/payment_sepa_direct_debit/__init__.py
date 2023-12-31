# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models

from thrive.addons.payment import reset_payment_provider


def uninstall_hook(cr, registry):
    reset_payment_provider(cr, registry, 'sepa_direct_debit')
