# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _
from thrive.addons.appointment.controllers.calendar_view import AppointmentCalendarView
from thrive.exceptions import AccessError
from thrive.http import request, route


class AppointmentHRCalendarView(AppointmentCalendarView):

    # Utility Methods
    # ----------------------------------------------------------

    def _prepare_appointment_type_anytime_values(self):
        appt_type_vals = super()._prepare_appointment_type_anytime_values()
        appt_type_vals.update(work_hours_activated=True)
        return appt_type_vals
