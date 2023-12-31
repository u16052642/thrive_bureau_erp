# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, fields, models, _lt

class Project(models.Model):
    _inherit = 'project.project'

    assets_count = fields.Integer('# Assets', compute='_compute_assets_count', groups='account.group_account_readonly')

    @api.depends('analytic_account_id')
    def _compute_assets_count(self):
        if not self.analytic_account_id:
            self.assets_count = 0
            return
        query = self.env['account.asset']._search([])
        query.add_where('account_asset.analytic_distribution ?| array[%s]', [str(account_id) for account_id in self.analytic_account_id.ids])
        query.order = None
        query_string, query_param = query.select(
            'jsonb_object_keys(analytic_distribution) as account_id',
            'COUNT(DISTINCT(id)) as asset_count',
        )
        query_string = f'{query_string} GROUP BY jsonb_object_keys(analytic_distribution)'
        self._cr.execute(query_string, query_param)
        data = {int(record.get('account_id')): record.get('asset_count') for record in self._cr.dictfetchall()}
        for project in self:
            project.assets_count = data.get(self.analytic_account_id.id, 0)

    # -------------------------------------
    # Actions
    # -------------------------------------

    def action_open_project_assets(self):
        query = self.env['account.asset']._search([])
        query.add_where('account_asset.analytic_distribution ? %s', [str(self.analytic_account_id.id)])
        assets = list(query)
        action = self.env["ir.actions.actions"]._for_xml_id("account_asset.action_account_asset_form")
        action.update({
            'views': [[False, 'tree'], [False, 'form'], [False, 'kanban']],
            'context': {'default_analytic_distribution': {self.analytic_account_id.id: 100}, 'default_asset_type': 'purchase'},
            'domain': [('id', 'in', assets)]
        })
        if(len(assets) == 1):
            action["views"] = [[False, 'form']]
            action["res_id"] = assets[0]
        return action

    # ----------------------------
    #  Project Updates
    # ----------------------------

    def _get_stat_buttons(self):
        buttons = super(Project, self)._get_stat_buttons()
        if self.user_has_groups('account.group_account_readonly'):
            buttons.append({
                'icon': 'pencil-square-o',
                'text': _lt('Assets'),
                'number': self.assets_count,
                'action_type': 'object',
                'action': 'action_open_project_assets',
                'show': self.assets_count > 0,
                'sequence': 54,
            })
        return buttons
