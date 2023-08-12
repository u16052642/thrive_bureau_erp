from . import models
from thrive import api, SUPERUSER_ID

def _create_demo_config_param(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].set_param('account_edi_proxy_client.demo', 'demo')
