# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from thrive.exceptions import AccessError

from thrive.addons.hr_holidays.tests.common import TestHrHolidaysCommon


class TestHrLeaveType(TestHrHolidaysCommon):

    def test_time_type(self):
        leave_type = self.env['hr.leave.type'].create({
            'name': 'Paid Time Off',
            'time_type': 'leave',
            'requires_allocation': 'no',
        })

        leave_1 = self.env['hr.leave'].create({
            'name': 'Doctor Appointment',
            'employee_id': self.employee_hruser_id,
            'holiday_status_id': leave_type.id,
            'date_from': (datetime.today() - relativedelta(days=1)),
            'date_to': datetime.today(),
            'number_of_days': 1,
        })
        leave_1.action_approve()

        self.assertEqual(
            self.env['resource.calendar.leaves'].search([('holiday_id', '=', leave_1.id)]).time_type,
            'leave'
        )

    def test_type_creation_right(self):
        # HrUser creates some holiday statuses -> crash because only HrManagers should do this
        with self.assertRaises(AccessError):
            self.env['hr.leave.type'].with_user(self.user_hruser_id).create({
                'name': 'UserCheats',
                'requires_allocation': 'no',
            })
