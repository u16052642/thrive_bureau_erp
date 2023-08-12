/** @thrive-module */
import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
const { coreTypes } = spreadsheet;

/** Plugin that link charts with Thrive menus. It can contain either the Id of the thrive menu, or its xml id. */
export default class ChartThriveMenuPlugin extends spreadsheet.CorePlugin {
    constructor() {
        super(...arguments);
        this.thriveMenuReference = {};
    }

    /**
     * Handle a spreadsheet command
     * @param {Object} cmd Command
     */
    handle(cmd) {
        switch (cmd.type) {
            case "LINK_THRIVE_MENU_TO_CHART":
                this.history.update("thriveMenuReference", cmd.chartId, cmd.thriveMenuId);
                break;
            case "DELETE_FIGURE":
                this.history.update("thriveMenuReference", cmd.id, undefined);
                break;
        }
    }

    /**
     * Get thrive menu linked to the chart
     *
     * @param {string} chartId
     * @returns {object | undefined}
     */
    getChartThriveMenu(chartId) {
        const menuId = this.thriveMenuReference[chartId];
        return menuId ? this.getters.getIrMenu(menuId) : undefined;
    }

    import(data) {
        if (data.chartThriveMenusReferences) {
            this.thriveMenuReference = data.chartThriveMenusReferences;
        }
    }

    export(data) {
        data.chartThriveMenusReferences = this.thriveMenuReference;
    }
}
ChartThriveMenuPlugin.modes = ["normal", "headless"];
ChartThriveMenuPlugin.getters = ["getChartThriveMenu"];

coreTypes.add("LINK_THRIVE_MENU_TO_CHART");
