# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models
from thrive.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super().session_info()
        result['dbuuid'] = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        return result

    def get_frontend_session_info(self):
        result = super().get_frontend_session_info()
        result['dbuuid'] = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        return result
