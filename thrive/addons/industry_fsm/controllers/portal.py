# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import http, _, SUPERUSER_ID
from thrive.exceptions import AccessError, MissingError
from thrive.http import request
from thrive.addons.portal.controllers import portal

import binascii


class CustomerPortal(portal.CustomerPortal):

    def _get_worksheet_data(self, task_sudo):
        # TO BE OVERRIDDEN
        return {}

    @http.route(['/my/task/<int:task_id>/worksheet',
                 '/my/task/<int:task_id>/worksheet/<string:source>',
                 '/my/task/<int:task_id>/worksheet/sign/<string:source>'], type='http', auth="public")
    def portal_worksheet_outdated(self, **kwargs):
        return request.redirect(request.httprequest.path.replace('/my/task/', '/my/tasks/'))

    @http.route(['/my/tasks/<int:task_id>/worksheet/sign/<string:source>'], type='json', auth="public", website=True)
    def portal_worksheet_sign(self, task_id, access_token=None, source=False, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            task_sudo = self._document_check_access('project.task', task_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid Task.')}

        if not task_sudo.has_to_be_signed():
            return {'error': _('The worksheet is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            task_sudo.write({
                'worksheet_signature': signature,
                'worksheet_signed_by': name,
            })
        except (TypeError, binascii.Error):
            return {'error': _('Invalid signature data.')}

        pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('industry_fsm.task_custom_report', [task_sudo.id])[0]
        task_sudo.message_post(body=_('The worksheet has been signed'), attachments=[('%s.pdf' % task_sudo.name, pdf)])
        return {
            'force_refresh': True,
            'redirect_url': task_sudo.get_portal_url(query_string=f'&source={source}'),
        }

    def _task_get_page_view_values(self, task, access_token, **kwargs):
        values = super()._task_get_page_view_values(task, access_token, **kwargs)
        values['source'] = kwargs.get('source')
        return values

    def _show_task_report(self, task_sudo, report_type, download):
        if not task_sudo.is_fsm:
            return super()._show_task_report(task_sudo, report_type, download)
        return self._show_report(model=task_sudo,
            report_type=report_type, report_ref='industry_fsm.task_custom_report', download=download)
