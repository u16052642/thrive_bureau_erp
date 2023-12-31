# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests.common import tagged, HttpCase


@tagged('-at_install', 'post_install')
class TestMailChannelExpand(HttpCase):

    def test_channel_expand_tour(self):
        testuser = self.env['res.users'].create({
            'email': 'testuser@testuser.com',
            'groups_id': [(6, 0, [self.ref('base.group_user')])],
            'name': 'Test User',
            'login': 'testuser',
            'password': 'testuser',
        })
        MailChannelAsUser = self.env['mail.channel'].with_user(testuser)
        channel_info = MailChannelAsUser.channel_create(name="test-mail-channel-expand-tour", group_id=self.ref('base.group_user'))
        channel = MailChannelAsUser.browse(channel_info['id'])
        channel.channel_fold('folded')
        channel.message_post(
            body="<p>test-message-mail-channel-expand-tour</p>",
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )
        # clear all bus notifications, so that tour does not replay old notifications
        # on a more recent state with init_messaging
        self.env['bus.bus'].search([]).unlink()
        self.start_tour("/web", 'mail_enterprise/static/tests/tours/mail_channel_expand_test_tour.js', login='testuser')
