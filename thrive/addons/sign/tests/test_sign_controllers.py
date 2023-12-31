# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
import json
from unittest.mock import patch

from .sign_request_common import SignRequestCommon
from thrive.tests.common import HttpCase
from thrive.addons.sign.controllers.main import Sign
from thrive.exceptions import ValidationError
from thrive.addons.website.tools import MockRequest
from thrive.tests import tagged

class TestSignControllerCommon(SignRequestCommon, HttpCase):
    def setUp(self):
        super().setUp()
        self.SignController = Sign()

    def _json_url_open(self, url, data, **kwargs):
        data = {
            "id": 0,
            "jsonrpc": "2.0",
            "method": "call",
            "params": data,
        }
        headers = {
            "Content-Type": "application/json",
            **kwargs.get('headers', {})
        }
        return self.url_open(url, data=json.dumps(data).encode(), headers=headers)


@tagged('post_install', '-at_install')
class TestSignController(TestSignControllerCommon):
    # test float auto_field display
    def test_sign_controller_float(self):
        sign_request = self.create_sign_request_no_item(signer=self.partner_1, cc_partners=self.partner_4)
        text_type = self.env['sign.item.type'].search([('name', '=', 'Text')])
        # the partner_latitude expects 7 zeros of decimal precision
        text_type.auto_field = 'partner_latitude'
        token_a = self.env["sign.request.item"].search([('sign_request_id', '=', sign_request.id)]).access_token
        with MockRequest(sign_request.env):
            values = self.SignController.get_document_qweb_context(sign_request.id, token=token_a)
            sign_type = list(filter(lambda sign_type: sign_type["name"] == "Text", values["sign_item_types"]))[0]
            latitude = sign_type["auto_value"]
            self.assertEqual(latitude, 0)

    # test auto_field with wrong partner field
    def test_sign_controller_dummy_fields(self):
        text_type = self.env['sign.item.type'].search([('name', '=', 'Text')])
        # we set a dummy field that raises an error
        with self.assertRaises(ValidationError):
            text_type.auto_field = 'this_is_not_a_partner_field'

    # test auto_field with multiple sub steps
    def test_sign_controller_multi_step_auto_field(self):
        self.partner_1.company_id = self.env.ref('base.main_company')
        self.partner_1.company_id.country_id = self.env.ref('base.be').id
        sign_request = self.create_sign_request_no_item(signer=self.partner_1, cc_partners=self.partner_4)
        text_type = self.env['sign.item.type'].search([('name', '=', 'Text')])
        text_type.auto_field = 'company_id.country_id.name'
        token_a = self.env["sign.request.item"].search([('sign_request_id', '=', sign_request.id)]).access_token
        with MockRequest(sign_request.env):
            values = self.SignController.get_document_qweb_context(sign_request.id, token=token_a)
            sign_type = list(filter(lambda sign_type: sign_type["name"] == "Text", values["sign_item_types"]))[0]
            country = sign_type["auto_value"]
            self.assertEqual(country, "Belgium")

    def test_sign_request_requires_auth_when_credits_are_available(self):
        sign_request = self.create_sign_request_1_role_sms_auth(self.partner_1, self.env['res.partner'])
        sign_request_item = sign_request.request_item_ids[0]

        self.assertFalse(sign_request_item.signed_without_extra_auth)
        self.assertEqual(sign_request_item.role_id.auth_method, 'sms')

        sign_vals = self.create_sign_values(sign_request.template_id.sign_item_ids, sign_request_item.role_id.id)
        with patch('thrive.addons.iap.models.iap_account.IapAccount.get_credits', lambda self, x: 10):
            response = self._json_url_open(
                '/sign/sign/%d/%s' % (sign_request.id, sign_request_item.access_token),
                data={'signature': sign_vals}
            ).json()['result']

            self.assertFalse(response.get('success'))
            self.assertTrue(sign_request_item.state, 'sent')
            self.assertFalse(sign_request_item.signed_without_extra_auth)

    def test_sign_request_allows_no_auth_when_credits_are_not_available(self):
        sign_request = self.create_sign_request_1_role_sms_auth(self.partner_1, self.env['res.partner'])
        sign_request_item = sign_request.request_item_ids[0]

        self.assertFalse(sign_request_item.signed_without_extra_auth)
        self.assertEqual(sign_request_item.role_id.auth_method, 'sms')

        sign_vals = self.create_sign_values(sign_request.template_id.sign_item_ids, sign_request_item.role_id.id)
        with patch('thrive.addons.iap.models.iap_account.IapAccount.get_credits', lambda self, x: 0):
            response = self._json_url_open(
                '/sign/sign/%d/%s' % (sign_request.id, sign_request_item.access_token),
                data={'signature': sign_vals}
            ).json()['result']

            self.assertTrue(response.get('success'))
            self.assertTrue(sign_request_item.state, 'completed')
            self.assertTrue(sign_request.state, 'done')
            self.assertTrue(sign_request_item.signed_without_extra_auth)
