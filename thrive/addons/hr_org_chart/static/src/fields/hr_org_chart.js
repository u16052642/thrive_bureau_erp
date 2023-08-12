/** @thrive-module */

import {Field} from '@web/views/fields/field';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePopover } from "@web/core/popover/popover_hook";

const { Component, onWillStart, onWillRender, useState } = owl;

function useUniquePopover() {
    const popover = usePopover();
    let remove = null;
    return Object.assign(Object.create(popover), {
        add(target, component, props, options) {
            if (remove) {
                remove();
            }
            remove = popover.add(target, component, props, options);
            return () => {
                remove();
                remove = null;
            };
        },
    });
}

class HrOrgChartPopover extends Component {
    async setup() {
        super.setup();

        this.rpc = useService('rpc');
        this.orm = useService('orm');
        this.actionService = useService("action");
    }

    /**
     * Get subordonates of an employee through a rpc call.
     *
     * @private
     * @param {integer} employee_id
     * @returns {Promise}
     */
    async _getSubordinatesData(employee_id, type) {
        const subData = await this.rpc(
            '/hr/get_subordinates',
            {
                employee_id: employee_id,
                subordinates_type: type,
                context: Component.env.session.user_context,
            }
        );
        return subData;
    }

    /**
     * Redirect to the employee form view.
     *
     * @private
     * @param {MouseEvent} event
     * @returns {Promise} action loaded
     */
    async _onEmployeeRedirect(employeeId) {
        const action = await this.orm.call('hr.employee', 'get_formview_action', [employeeId]);
        this.actionService.doAction(action); 
    }

    /**
     * Redirect to the sub employee form view.
     *
     * @private
     * @param {MouseEvent} event
     * @returns {Promise} action loaded
     */
    async _onEmployeeSubRedirect(event) {
        const employee_id = parseInt(event.currentTarget.dataset.employeeId);
        const type = event.currentTarget.dataset.type || 'direct';
        if (!employee_id) {
            return {};
        }
        const subData = await this._getSubordinatesData(employee_id, type);
        const domain = [['id', 'in', subData]];
        var action = await this.orm.call('hr.employee', 'get_formview_action', [employee_id]);
        action = Object.assign(action, {
            'name': this.env._t('Team'),
            'view_mode': 'kanban,list,form',
            'views':  [[false, 'kanban'], [false, 'list'], [false, 'form']],
            'domain': domain,
            'context': {
                'default_parent_id': employee_id,
            }
        });
        delete action['res_id'];
        this.actionService.doAction(action);
    }
}
HrOrgChartPopover.template = 'hr_org_chart.hr_orgchart_emp_popover';

export class HrOrgChart extends Field {
    async setup() {
        super.setup();

        this.rpc = useService('rpc');
        this.orm = useService('orm');
        this.actionService = useService("action");
        this.popover = useUniquePopover();

        this.jsonStringify = JSON.stringify;

        this.state = useState({'employee_id': null});

        onWillStart(this.handleComponentUpdate.bind(this));
        onWillRender(this.handleComponentUpdate.bind(this));
    }

    /**
     * Called on start and on render
     */
    async handleComponentUpdate() {
        this.employee = this.props.record.data;
        // the widget is either dispayed in the context of a hr.employee form or a res.users form
        this.state.employee_id = this.employee.employee_ids !== undefined ? this.employee.employee_ids.resIds[0] : this.employee.id;
        const forceReload = this.lastRecord !== this.props.record;
        this.lastRecord = this.props.record;
        await this.fetchEmployeeData(this.state.employee_id, forceReload);
    }

    async fetchEmployeeData(employeeId, force = false) {
        if (!employeeId) {
            this.managers = [];
            this.children = [];
            if (this.view_employee_id) {
                this.render(true);
            }
            this.view_employee_id = null;
        } else if (employeeId !== this.view_employee_id || force) {
            this.view_employee_id = employeeId;
            var orgData = await this.rpc(
                '/hr/get_org_chart',
                {
                    employee_id: employeeId,
                    context: Component.env.session.user_context,
                }
            );
            if (Object.keys(orgData).length === 0) {
                orgData = {
                    managers: [],
                    children: [],
                }
            }
            this.managers = orgData.managers;
            this.children = orgData.children;
            this.managers_more = orgData.managers_more;
            this.self = orgData.self;
            this.render(true);
        }
    }

    _onOpenPopover(event, employee) {
        this.popover.add(
            event.currentTarget,
            this.constructor.components.Popover,
            {employee},
            {closeOnClickAway: true}
        );
    }

    /**
     * Redirect to the employee form view.
     *
     * @private
     * @param {MouseEvent} event
     * @returns {Promise} action loaded
     */
    async _onEmployeeRedirect(employeeId) {
        const action = await this.orm.call('hr.employee', 'get_formview_action', [employeeId]);
        this.actionService.doAction(action); 
    }

    async _onEmployeeMoreManager(managerId) {
        await this.fetchEmployeeData(managerId);
        this.state.employee_id = managerId;
    }
}

HrOrgChart.components = {
    Popover: HrOrgChartPopover,
};

HrOrgChart.template = 'hr_org_chart.hr_org_chart';

registry.category("fields").add("hr_org_chart", HrOrgChart);
