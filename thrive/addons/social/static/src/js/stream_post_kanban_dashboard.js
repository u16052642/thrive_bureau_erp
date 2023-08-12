/** @thrive-module **/

import { formatInteger } from '@web/views/fields/formatters';
import { useService } from '@web/core/utils/hooks';

const { Component, onMounted, onWillUnmount, useRef } = owl;

export class StreamPostDashboard extends Component {

    setup() {
        super.setup();
        this.dashboard = useRef('dashboard');
        this.notification = useService('notification');
        this.orm = useService('orm');
        this.popover = [];

        onMounted(() => this._initPopover());

        onWillUnmount(() => this._disposePopover());
    }

    formatStatValue(statValue) {
        return formatInteger(statValue);
    }

    _onRelinkAccount(event) {
        const mediaId = event.currentTarget.dataset.mediaId;
        if (this.props.isSocialManager) {
            this.orm.call('social_media', 'action_add_account', mediaId).then((action) => {
                document.location = action.url;
            });
        } else {
            this.notification.add(
                this.env._t('Sorry, you\'re not allowed to re-link this account, please contact your administrator.'),
                {type: 'danger'}
            );
        }
    }

    _initPopover() {
        this.dashboard.el.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => {
            this.popover.push(new Popover(el, {
                trigger: 'hover',
                delay: {show: 500, hide: 0},
            }));
        });
    }

    _disposePopover() {
        this.popover.forEach((popover) => {
            popover.dispose();
        })
    }

    _hasAudience(account) {
        return true;
    }

    _hasEngagement(account) {
        return true;
    }

    _hasStories(account) {
        return true;
    }

}

StreamPostDashboard.template = 'social.KanbanDashboard';
StreamPostDashboard.props = {
    accounts: Array,
    isSocialManager: Boolean,
};
