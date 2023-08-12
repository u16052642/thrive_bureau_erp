# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class Attendee(models.Model):
    _inherit = 'calendar.attendee'

    def _compute_mail_tz(self):
        toupdate = self.filtered(lambda r: r.event_id.appointment_type_id.appointment_tz)
        for attendee in toupdate:
            attendee.mail_tz = attendee.event_id.appointment_type_id.appointment_tz
        super(Attendee, self - toupdate)._compute_mail_tz()
