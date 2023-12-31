#-*- coding:utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, SUPERUSER_ID

from . import models
from . import wizard
from . import controllers
from . import report


def _post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    env['res.company'].search([])._create_dashboard_notes()
