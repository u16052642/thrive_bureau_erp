# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from markupsafe import Markup

from thrive import _, models


class ProposeChange(models.TransientModel):
    _inherit = 'propose.change'

    def default_get(self, fields_list):
        res = super().default_get(fields_list=fields_list)
        if 'step_id' in fields_list:
            wo = self.env['quality.check'].browse(res.get('step_id')).workorder_id
            eco = self.env['mrp.eco'].sudo().search([
                ('bom_id', '=', wo.production_id.bom_id.id),
                ('state', 'in', ('confirmed', 'progress')),
            ])
            if eco:
                res['eco_type_id'] = eco.type_id.id
        return res

    def _get_eco(self):
        self.ensure_one()
        eco = self.env['mrp.eco'].sudo().search([
            ('bom_id', '=', self.workorder_id.production_id.bom_id.id),
            ('state', 'in', ('confirmed', 'progress')),
        ], limit=1)
        type_id = self.env.ref('mrp_workorder_plm.ecotype_workorder')
        if not eco:
            name = self.workorder_id.name + "/"
            name += self.workorder_id.production_id.name
            eco = self.env['mrp.eco'].sudo().create({
                'name': name,
                'product_tmpl_id': self.workorder_id.product_id.product_tmpl_id.id,
                'bom_id': self.workorder_id.production_id.bom_id.id,
                'type_id': type_id.id,
                'stage_id': self.env['mrp.eco.stage'].sudo().search([
                    ('type_ids', 'in', type_id.ids),
                ], limit=1).id
            })
            eco.action_new_revision()
        return eco

    def _do_update_step(self):
        eco = self._get_eco()
        super()._do_update_step(notify_bom=False)
        # get the step on the new bom related to the one we want to update
        new_step = eco.new_bom_id.operation_ids.quality_point_ids.filtered(lambda p: p._get_comparison_values() == self.step_id.point_id._get_comparison_values())
        new_step.note = self.note
        # Write reason in chatter
        if new_step:
            tl_text = _("New Instruction suggested by %(user_name)s", user_name=self._workorder_name())
            body = Markup("<b>%s</b>") % tl_text
            if self.comment:
                tl_text = _("Reason:")
                body += Markup("<br/><b>%s</b> %s") % (tl_text, self.comment)
            new_step.message_post(body=body)

    def _do_remove_step(self):
        eco = self._get_eco()
        super()._do_remove_step(notify_bom=False)
        # get the step on the new bom related to the one we want to delete
        new_step = eco.new_bom_id.operation_ids.quality_point_ids.filtered(lambda p: p._get_comparison_values() == self.step_id.point_id._get_comparison_values())
        new_step.unlink()
        # Leave a note in the old step's chatter telling why it should be removed.
        old_step = self.step_id.point_id
        if old_step:
            tl_text = _("%(user_name)s suggests to delete this instruction", user_name=self._workorder_name())
            body = Markup("<b>%s</b>") % tl_text
            if self.comment:
                tl_text = _("Reason:")
                body += Markup("<br/><b>%s</b> %s") % (tl_text, self.comment)
            old_step.message_post(body=body)

    def _do_set_picture(self):
        eco = self._get_eco()
        super()._do_set_picture(notify_bom=False)
        # get the step on the new bom related to the one we want to delete
        new_step = eco.new_bom_id.operation_ids.quality_point_ids.filtered(lambda p: p._get_comparison_values() == self.step_id.point_id._get_comparison_values())
        new_step.note = Markup("<img class='img-fluid' src=%s/>") % self.image_url(self, 'picture')
        new_step.source_document = 'step'
