# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from . import models
from . import wizard

from thrive import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    ICP = env['ir.config_parameter']
    ICP.set_param('google.custom_search.cx', False)
    ICP.set_param('google.custom_search.key', False)
