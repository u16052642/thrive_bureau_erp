# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _load_menus_blacklist(self):
        res = super()._load_menus_blacklist()
        if not (self.env.user.has_group('hr_attendance.group_hr_attendance_user') and self.env.user.has_group('hr_timesheet.group_hr_timesheet_user')):
            res.append(self.env.ref('hr_timesheet_attendance.menu_hr_timesheet_attendance_report').id)
        return res
