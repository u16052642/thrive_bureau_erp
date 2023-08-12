/** @thrive-module **/

import { patch } from "@web/core/utils/patch";
import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
import { IrMenuSelector } from "@spreadsheet_edition/assets/components/ir_menu_selector/ir_menu_selector";

const { LineBarPieConfigPanel, ScorecardChartConfigPanel, GaugeChartConfigPanel } =
    spreadsheet.components;

/**
 * Patch the chart configuration panel to add an input to
 * link the chart to an Thrive menu.
 */
function patchChartPanelWithMenu(PanelComponent, patchName) {
    patch(PanelComponent.prototype, patchName, {
        get thriveMenuId() {
            const menu = this.env.model.getters.getChartThriveMenu(this.props.figureId);
            return menu ? menu.id : undefined;
        },
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
        },
    });
    PanelComponent.components = {
        ...PanelComponent.components,
        IrMenuSelector,
    };
}
patchChartPanelWithMenu(LineBarPieConfigPanel, "document_spreadsheet.LineBarPieConfigPanel");
patchChartPanelWithMenu(GaugeChartConfigPanel, "document_spreadsheet.GaugeChartConfigPanel");
patchChartPanelWithMenu(
    ScorecardChartConfigPanel,
    "document_spreadsheet.ScorecardChartConfigPanel"
);
