# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models, _
from thrive.tools.misc import clean_context


class SurveyInvite(models.TransientModel):
    _inherit = "survey.invite"

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')

    def action_invite(self):
        self.ensure_one()
        if self.applicant_id:
            survey = self.survey_id.with_context(clean_context(self.env.context))

            if not self.applicant_id.response_id:
                self.applicant_id.write({
                    'response_id': survey._create_answer(partner=self.applicant_id.partner_id).id
                })

            partner = self.applicant_id.partner_id
            survey_link = survey._get_html_link(title=survey.title)
            partner_link = partner._get_html_link()
            content = _('The survey %(survey_link)s has been sent to %(partner_link)s', survey_link=survey_link, partner_link=partner_link)
            body = '<p>%s</p>' % content
            self.applicant_id.message_post(body=body)
        return super().action_invite()


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    applicant_id = fields.One2many('hr.applicant', 'response_id', string='Applicant')

    def _mark_done(self):
        thrivebot = self.env.ref('base.partner_root')
        for user_input in self:
            if user_input.applicant_id:
                body = _('The applicant "%s" has finished the survey.', user_input.applicant_id.partner_name)
                user_input.applicant_id.message_post(body=body, author_id=thrivebot.id)
        return super()._mark_done()
