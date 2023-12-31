# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    tag_ids = fields.Many2many('documents.tag')
    folder_id = fields.Many2one('documents.folder',
                                help="By defining a folder, the upload activities will generate a document")
