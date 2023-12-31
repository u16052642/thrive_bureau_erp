# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.test_mail.tests.test_mail_template import TestMailTemplateCommon
from thrive.tests import tagged


@tagged('mail_template', 'multi_lang')
class TestMailTemplateTools(TestMailTemplateCommon):

    def test_mail_template_preview_force_lang(self):
        test_record = self.env['mail.test.lang'].browse(self.test_record.ids)
        test_record.write({
            'lang': 'es_ES',
        })
        test_template = self.env['mail.template'].browse(self.test_template.ids)

        preview = self.env['mail.template.preview'].create({
            'mail_template_id': test_template.id,
            'resource_ref': test_record,
            'lang': 'es_ES',
        })
        self.assertEqual(preview.body_html, '<p>SpanishBody for %s</p>' % test_record.name)

        preview.write({'lang': 'en_US'})
        self.assertEqual(preview.body_html, '<p>EnglishBody for %s</p>' % test_record.name)
