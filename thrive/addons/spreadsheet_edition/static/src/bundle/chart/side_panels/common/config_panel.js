/** @thrive-module */

import { IrMenuSelector } from "@spreadsheet_edition/assets/components/ir_menu_selector/ir_menu_selector";

const { Component } = owl;

export class CommonThriveChartConfigPanel extends Component {
    get thriveMenuId() {
        const menu = this.env.model.getters.getChartThriveMenu(this.props.figureId);
        return menu ? menu.id : undefined;
    }
    /**
     * @param {number | undefined} thriveMenuId
     */
    updateThriveLink(thriveMenuId) {
        if (!thriveMenuId) {
            this.env.model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
                chartId: this.props.figureId,
                thriveMenuId: undefined,
            });
            return;
        }
        const menu = this.env.model.getters.getIrMenu(thriveMenuId);
        this.env.model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
            chartId: this.props.figureId,
            thriveMenuId: menu.xmlid || menu.id,
        });
    }
}

CommonThriveChartConfigPanel.template = "spreadsheet_edition.CommonThriveChartConfigPanel";
CommonThriveChartConfigPanel.components = { IrMenuSelector };
