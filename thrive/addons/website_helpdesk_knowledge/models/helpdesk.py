# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models, fields, _

class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    show_knowledge_base_article = fields.Boolean(compute="_compute_show_knowledge_base_article")
    website_article_id = fields.Many2one('knowledge.article', string='Article',
        help="Article on which customers will land by default, and to which the search will be restricted.")

    @api.depends('website_article_id')
    def _compute_show_knowledge_base_article(self):
        # 'show_knowledge_base_article' determines whether the help page of the website displays a link to articles.
        accessible_articles = self.env['knowledge.article'].search_count([], limit=1) > 0
        for team_sudo in self.sudo():
            team_sudo.show_knowledge_base_article = team_sudo.use_website_helpdesk_knowledge and accessible_articles

    @api.model
    def _get_knowledge_base_fields(self):
        return super()._get_knowledge_base_fields() + ['show_knowledge_base_article']

    def _helpcenter_filter_types(self):
        res = super()._helpcenter_filter_types()
        if not self.show_knowledge_base_article:
            return res

        res['knowledge'] = _('Articles')
        return res
