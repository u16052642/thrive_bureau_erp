# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResUsersSettings(models.Model):
    _inherit = 'res.users.settings'

    is_discuss_sidebar_category_livechat_open = fields.Boolean("Is category livechat open", default=True)
