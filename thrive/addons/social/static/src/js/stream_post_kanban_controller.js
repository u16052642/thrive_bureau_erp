/** @thrive-module **/

import { AddSocialStreamDialog } from './add_stream_modal';
import { NewContentRefreshBanner } from './stream_post_kanban_refresh_banner';
import { StreamPostDashboard } from './stream_post_kanban_dashboard';

import { KanbanController } from '@web/views/kanban/kanban_controller';
import { sprintf } from '@web/core/utils/strings';
import { useService } from '@web/core/utils/hooks';

const { onWillStart, useEffect, useSubEnv, useState } = owl;

export class StreamPostKanbanController extends KanbanController {

    setup() {
        super.setup();
        this.company = useService('company');
        this.dialog = useService('dialog');
        this.orm = useService('orm');
        this.notification = useService('notification');
        this.state = useState({
            refreshRequired: false,
        });
        this.user = useService('user');
        useSubEnv({
            refreshStats: this._onRefreshStats.bind(this)
        });

        useEffect((addStreamLink) => {
            if (addStreamLink) {
                addStreamLink.addEventListener('click', this._onNewStream.bind(this));
            }
        }, () => [document.querySelector('.o_social_js_add_stream')]);

        onWillStart(async () => {
            this.isSocialManager = await this.user.hasGroup("social.group_social_manager");
            this.hasAccounts = await this.orm.searchCount('social.account', []) > 0;
            this.accounts = await this.model._loadAccountsStats();
        });
        onWillStart(() => this._onRefreshStats());
    }

    async _onRefreshStats() {
        this.model._refreshStreams().then((result) => {
            this.state.refreshRequired = result;
        });
        this.model._refreshAccountsStats().then((result) => {
            this.accounts = result;
        });
    }

    _refreshView() {
        this.state.refreshRequired = false;
        this.model.load();
    }

    _onNewPost() {
        this.actionService.doAction({
            name: this.env._t('New Post'),
            type: 'ir.actions.act_window',
            res_model: 'social.post',
            views: [[false, "form"]],
        });
    }

    _onNewStream() {
        if (this.accounts.length > 0 || this.isSocialManager) {
            this._addNewStream();
        } else {
            this.notification.add(
                this.env._t("No social accounts configured, please contact your administrator."),
                { type: 'danger' }
            );
        }
    }

    _addNewStream() {
        this._fetchSocialMedia().then((socialMedia) =>
            this.dialog.add(AddSocialStreamDialog, {
                title: this.env._t('Add a Stream'),
                isSocialManager: this.isSocialManager,
                socialMedia: socialMedia,
                socialAccounts: this.accounts,
                companies: this._getCompanies(),
                onSaved: this._onStreamAdded.bind(this),
            })
        )
    }

    async _onStreamAdded(stream) {
        const streams = await this.orm.searchRead(
            'social.stream',
            [
                ['id', '=', stream.data.id],
                ['stream_post_ids', '=', false]
            ],
            ['name']);
        if (streams.length) {
            this.notification.add(
                sprintf(this.env._t('It will appear in the Feed once it has posts to display.')),
                {
                    title: sprintf(this.env._t('Stream Added (%s)'), streams[0].name),
                    type: 'success',
                }
            )
        } else {
            this.model.load();
        }
    }

    /**
     * Fetches media on which you can add remote accounts and streams.
     * We check the fact that they handle streams.
     *
     * @private
     */
    async _fetchSocialMedia() {
        if (this.socialMedia) {
            return this.socialMedia;
        } else {
            this.socialMedia = await this.orm.searchRead(
                'social.media',
                [['has_streams', '=', 'True']],
                ['id', 'name'],
            );
            return this.socialMedia;
        }
    }

    /**
     * Return the list of allowed companies for the current users.
     * The first element of the array is the current selected company.
     *
     * @private
     * @param {Array} [{id: company_id, name: company_name}, ...]
     */
    _getCompanies() {
        const companies = this.company.availableCompanies;
        return this.company.allowedCompanyIds.map(companyId => companies[companyId]);
    }

}

StreamPostKanbanController.components = {
    ...KanbanController.components,
    NewContentRefreshBanner,
    StreamPostDashboard,
};
StreamPostKanbanController.template = 'social.SocialKanbanView';
