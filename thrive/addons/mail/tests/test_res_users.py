# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from psycopg2 import IntegrityError

from thrive.addons.mail.tests.common import MailCommon, mail_new_test_user
from thrive.tools import mute_logger


class TestUser(MailCommon):

    @mute_logger('thrive.sql_db')
    def test_notification_type_constraint(self):
        with self.assertRaises(IntegrityError, msg='Portal user can not receive notification in Thrive'):
            mail_new_test_user(
                self.env,
                login='user_test_constraint_2',
                name='Test User 2',
                email='user_test_constraint_2@test.example.com',
                notification_type='inbox',
                groups='base.group_portal',
            )
