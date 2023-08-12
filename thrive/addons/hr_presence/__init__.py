# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from . import models

from thrive import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    email = env['ir.config_parameter'].get_param('hr_presence.hr_presence_control_email')
    ip = env['ir.config_parameter'].get_param('hr_presence.hr_presence_control_ip')

    if not email and not ip:
        env['ir.config_parameter'].sudo().set_param('hr_presence.hr_presence_control_email', True)
