/** @thrive-module alias=account_online_synchronization.thrive_fin_connector **/
"use strict";

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { getCookie } from "web.utils.cookies";

const actionRegistry = registry.category('actions');
/* global ThriveFin */

function ThriveFinConnector(parent, action) {
    const id = action.id;
    action.params.colorScheme = getCookie("color_scheme");
    let mode = action.params.mode || 'link';
    // Ensure that the proxyMode is valid
    const modeRegexp = /^[a-z0-9-_]+$/i;
    if (!modeRegexp.test(action.params.proxyMode)) {
        return;
    }
    let url = 'https://' + action.params.proxyMode + '.thrivefin.com/proxy/v1/thrivefin_link';

    loadJS(url)
        .then(function () {
            // Create and open the iframe
            let params = {
                data: action.params,
                proxyMode: action.params.proxyMode,
                onEvent: function (event, data) {
                    let rpcUrl = '/web/dataset/call_kw/account.online.link'
                    switch (event) {
                        case 'close':
                            return;
                        case 'reload':
                            return parent.services.action.doAction({type: 'ir.actions.client', tag: 'reload'});
                        case 'notification':
                            parent.services.notification.add(data.message, data);
                            break;
                        case 'exchange_token':
                            parent.services.rpc(rpcUrl + '/exchange_token', {
                                model: 'account.online.link',
                                method: 'exchange_token',
                                args: [[id], data],
                                kwargs: {}
                            })
                            break;
                        case 'success':
                            mode = data.mode || mode;
                            return parent.services.rpc(rpcUrl + '/success', {
                                model: 'account.online.link',
                                method: 'success',
                                args: [[id], mode, data],
                                kwargs: {}
                            })
                            .then(action => parent.services.action.doAction(action));
                        default:
                            return;
                    }
                },
                onAddBank: function () {
                    // If the user doesn't find his bank
                    return parent.services.rpc("/web/dataset/call_kw/account.online.link/create_new_bank_account_action", {
                        model: 'account.online.link',
                        method: 'create_new_bank_account_action',
                        args: [],
                        kwargs: {}
                    })
                    .then(action => parent.services.action.doAction(action, {replace_last_action: true}));
                }
            }
            ThriveFin.create(params);
            ThriveFin.open();
        });
    return;
}

actionRegistry.add('thrive_fin_connector', ThriveFinConnector);

export default ThriveFinConnector;
