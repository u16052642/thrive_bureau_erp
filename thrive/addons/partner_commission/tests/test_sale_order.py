# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.fields import Command
from thrive.tests import Form, tagged
from thrive.addons.partner_commission.tests.setup import TestCommissionsSetup


@tagged('commission_sale')
class TestSaleOrder(TestCommissionsSetup):
    def test_referrer_commission_plan_changed(self):
        """When the referrer's commission plan changes, its new commission plan should be set on the sale order."""
        self.referrer.commission_plan_id = self.gold_plan

        form = Form(self.env['sale.order'].with_user(self.salesman).with_context(tracking_disable=True))
        form.partner_id = self.customer
        form.referrer_id = self.referrer
        so = form.save()

        self.assertEqual(so.commission_plan_id, self.gold_plan)

        # Update referrer's commission plan.
        self.referrer.commission_plan_id = self.silver_plan
        self.assertEqual(so.commission_plan_id, self.silver_plan)

    def test_referrer_grade_changed(self):
        """When the referrer's grade changes, its new commission plan should be set on the sale order."""
        self.referrer.grade_id = self.gold
        self.referrer._onchange_grade_id()
        form = Form(self.env['sale.order'].with_user(self.salesman).with_context(tracking_disable=True))
        form.partner_id = self.customer
        form.referrer_id = self.referrer
        so = form.save()

        # Demote the referrer to silver.
        self.referrer.grade_id = self.silver
        self.referrer._onchange_grade_id()
        self.assertEqual(so.commission_plan_id, self.silver_plan)

    def test_so_data_forwarded_to_sub(self):
        """Some data should be forwarded from the sale order to the subscription."""
        self.referrer.commission_plan_id = self.gold_plan

        form = Form(self.env['sale.order'].with_user(self.salesman).with_context(tracking_disable=True))
        form.partner_id = self.customer
        form.referrer_id = self.referrer
        # form.commission_plan_frozen = False
        form.recurrence_id = self.recurrence_year

        with form.order_line.new() as line:
            line.name = self.worker.name
            line.product_id = self.worker
            line.product_uom_qty = 1

        so = form.save()
        so.action_confirm()

        # check that inverse field is working
        so.commission_plan_id = self.silver_plan
        self.assertEqual(so.commission_plan_id, self.silver_plan)
        self.assertEqual(so.commission_plan_frozen, True)

    def test_so_data_forwarded_to_invoice(self):
        """Some data should be forwarded from the sale order to the invoice."""
        self.referrer.commission_plan_id = self.gold_plan

        form = Form(self.env['sale.order'].with_user(self.salesman).with_context(tracking_disable=True))
        form.partner_id = self.customer
        form.referrer_id = self.referrer
        # We test the non recurring flow: recurring_invoice is False on the product
        self.worker.recurring_invoice = False
        with form.order_line.new() as line:
            line.name = self.worker.name
            line.product_id = self.worker
            line.product_uom_qty = 1

        so = form.save()
        so.action_confirm()

        inv = self.env['account.move'].create(so._prepare_invoice())

        self.assertEqual(inv.referrer_id, so.referrer_id)

    def test_compute_commission(self):
        self.referrer.commission_plan_id = self.gold_plan

        form = Form(self.env['sale.order'].with_user(self.salesman).with_context(tracking_disable=True))
        form.partner_id = self.customer
        form.referrer_id = self.referrer
        # We test the non recurring flow: recurring_invoice is False on the product
        self.worker.recurring_invoice = False
        with form.order_line.new() as line:
            line.name = self.worker.name
            line.product_id = self.worker
            line.product_uom_qty = 2

        so = form.save()
        so.pricelist_id = self.eur_20
        so.action_confirm()

        self.assertEqual(so.commission, 150)

    def test_so_referrer_id_to_invoice(self):
        """Referrer_id should be the same in the new created invoice"""
        self.referrer.commission_plan_id = self.gold_plan
        self.worker.recurring_invoice = False # test on a non recurring SO
        form = Form(self.env['sale.order'].with_user(self.salesman).with_context(tracking_disable=True))
        form.partner_id = self.customer
        form.referrer_id = self.referrer

        with form.order_line.new() as line:
            line.name = self.worker.name
            line.product_id = self.worker
            line.product_uom_qty = 1

        so = form.save()
        so.action_confirm()

        invoice_wizard = self.env['sale.advance.payment.inv'].with_context(tracking_disable=True).create({
            'advance_payment_method': 'fixed',
            'sale_order_ids': [Command.set(so.ids)],
            'fixed_amount': 100,
        })

        inv = invoice_wizard._create_invoices(so)
        self.assertEqual(inv.referrer_id, so.referrer_id)
