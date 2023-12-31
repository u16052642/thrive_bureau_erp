/** @thrive-module **/
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

import { Component } from "@thrive/owl";

export class DomainSelectorBranchOperator extends Component {
    onOperatorSelected(operator) {
        this.props.node.update(operator);
    }
}
DomainSelectorBranchOperator.components = {
    Dropdown,
    DropdownItem,
};
DomainSelectorBranchOperator.template = "web.DomainSelectorBranchOperator";
DomainSelectorBranchOperator.props = {
    node: Object,
    readonly: Boolean,
    showCaret: {
        type: Boolean,
        optional: true,
    },
};
