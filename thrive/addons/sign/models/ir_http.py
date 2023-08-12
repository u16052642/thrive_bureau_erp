# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models
from thrive.http import request

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @api.model
    def get_frontend_session_info_sign(self):
        frontend_session_info = super().get_frontend_session_info()
        frontend_session_info.update({
            'user_context': request.env.context
        })
        return frontend_session_info
