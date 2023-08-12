# -*- encoding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import json

from thrive import fields, models


class QualityCheck(models.Model):
    _inherit = "quality.check"

    boxes = fields.Char(compute='_compute_boxes')

    def _compute_boxes(self):
        for qc in self:
            triggers = qc.workcenter_id.trigger_ids
            box_dict = {}
            for trigger in triggers:
                box = trigger.device_id.iot_id.ip
                box_dict.setdefault(box, [])
                box_dict[box].append([trigger.device_id.identifier, trigger.key, trigger.action])
            qc.boxes = json.dumps(box_dict)

    def action_print(self):
        quality_point_id = self.point_id
        res = super().action_print()

        if quality_point_id.device_id:
            res['device_id'] = quality_point_id.device_id.id

        return res

    def _get_fields_list_for_tablet(self):
        result = super()._get_fields_list_for_tablet()
        result.append('boxes')
        return result